Title: Mounting a FUSE filesystem in Heroku
Date: 2017-02-06
Category: field-notes
Tags: Heroku, FUSE, python, docker
Slug: heroku_fuse_mount
Author: Phil Elson


This evening I'm going to take a different approach to how I would normally blog.

Rather than reporting the results of a technical investigation or highlighting a new/shiny package, I wanted to
paint a realistic picture of the technical exploration process.

As it happens, this particular investigation consumed a couple of hours and appears to have drawn an unsuccessful
result. Despite this, the learnings are invaluable as they will be directly and immediately applicable to other areas of my work.

<!-- PELICAN_END_SUMMARY -->

## The problem

I run a number of services on Heroku. It's an amazing platform for rapid prototyping of (mostly web) applications. The beauty of Heroku is the ease of deployment as well as its availability, scalability and cost.

I have one particular application on Heroku that draws statistics from a moderately sized, slow paced, filestore.
Unfortunately, since all storage on Heroku is ephemeral, that means I must fetch the data at least once every 24 hours (when Heroku restarts the container) to recompute my statistics (which are cached for application performance). Fetching the data is a costly operation, and I'd rather avoid it if possible.

Instead of fetching the data on a daily basis, I'd like to have a third-party filestore that can be used from within the Heroku application for its statistics generation.
I'd also like to use the store for the cache (which itself can be mem-cached/cached to the ephemeral Heroku disk).
In order to invalidate the cache I will want an efficient means of getting a checksum or pertinent fstat info.
The detail here isn't important, suffice to say I'd just like *some* persistence my source data for an otherwise stateless application.


## The proposal

Having read a little in the past about libfuse, it seemed that using FUSE to mount a networked resource would be a great match for the problem.
Because I have a few GB lying around on Dropbox, and there appeared to be a python based Dropbox-fuse client (ff4d), I decided to investigate the feasibility of mounting my Dropbox directory inside my Heroku application. 
Other options would have worked just as a well, including an S3 bucket (with s3fs-fuse), or a direct ssh connection (with sshfs).

I had also read a little bit about Heroku's new Docker container registry and runtime environment (https://devcenter.heroku.com/articles/container-registry-and-runtime) and thought this would be a great opportunity to shorten the deployment cycle.


## The findings

### Mounting a Dropbox directory through ff4d

The first step is to get FUSE up-and-running on my own machine (OSX). libfuse is the first thing in a while
that I've not been able to get hold of through conda, so I ended up dusting off my homebrew installation and going through
a pretty hefty update. Once complete I tried:

    brew install libfuse

With no success. Turns out that osxfuse is a thing, and so I:

    brew install osxfuse

Again, no luck, but homebrew does point me in the direction of a cask version (pre-compiled, rather than building it from source on my machine). I'm pretty keen to get going with this, so I go ahead and install the cask version:

    brew install Caskroom/cask/osxfuse

After a short wait, the result is positive, and it looks like I have a local FUSE installation.

Next, I want to try it out. Rather than choose to do something simple, I go straight for the jugular and try to get a Dropbox FUSE mount working. I clone https://github.com/realriot/ff4d and get myself set up with a legacy python installation (in a clean environment named "ff4d_py2":

    conda create -n ff4d_py2 python=2 pip
    source activate ff4d_py2
    pip install dropbox

I take a note of the dependency on a legacy version of Python, and vow to submit a merge request making the codebase python (3) compatible should I want to turn this proof-of-concept into something more.

Next, I create a "Dropbox API" -> "Full Dropbox" application on https://www.dropbox.com/developers/apps/create and run:

    python getDropboxAccessToken.py

I follow on the on-screen prompts and am eventually rewarded with an OAuth token that I store securely.
With my token in hand:

    mkdir foobar
    python ff4d.py  ./foobar -ap <my_token>

Gives me a directory called foobar containing my Dropbox content, and reminds me that I can delete nearly a GB of images that
were shared with colleagues on my Dropbox account. As I delete the files (```rm -rf ./foobar/my_image_directory```) I'm aware that
there are a number of 404 error type messages being logged by ff4d.py - I take a note that there is something that needs deeper investigation here.

So there we have it, a locally mounted Dropbox folder sitting on my OSX machine, thanks to ff4d.
Now, I want to create a webapp that can show the contents of my directory (as a proof-of-concept), and to replicate this
setup in a docker container, and then ultimately in a Heroku web app deployment.


### Creating the webapp

I'm a big fan of [tornado](http://www.tornadoweb.org/en/stable/), and since the application that could benefit from
access to my Dropbox mount is also using tornado I put together a quick web-app to browse the directory.

I'd assumed that creating a http handler that allows directory listing would be built-in to tornado, but it appears not,
so I ended up re-using code from https://github.com/imom0/SimpleTornadoServer/blob/master/SimpleTornadoServer.py (BSD-3)
to allow me to navigate my directories from within the webapp.

In order for my webapp and ff4d mount to be run on the same process within Heroku (not the only option - it is easy enough to create new processes on Heroku, I just like the ability to control them all from a single process) I need to get the webapp to
mount the Dropbox directory itself.
Since mounting through ff4d is blocking, I am going to need to run one 2 IOLoops, one on the main thread (for tornado) and the other in a ThreadPoolExecutor managed thread (for ff4d).

Getting another thread to run a blocking script whilst still running a responsive tornado main IOLoop thread is something I have done a few times now.
In other situations I have wanted to communicate through Kafka ((example)[http://stackoverflow.com/a/40602866/741316]) in my tornado application, and in another application I wanted the ability to (optionally) spawn a Dask scheduler, workers and client. Truth be told, in most of these situations processes are a better choice, but I digress.

Getting a tornado webapp to run a blocking process in another thread is surprisingly easy.
We need a ThreadPool, and an asynchronous function that can run on the main thread:

    
    @tornado.gen.coroutine
    def async(executor, function, *args, **kwargs):
        yield executor.submit(function, *args, **kwargs)

    thread_pool = ThreadPoolExecutor(1)
    tornado.ioloop.IOLoop.current().spawn_callback(async, thread_pool, start_mount, mount_dir=mount_dir)


The function itself is fairly trivial, and simply spawns a sub-process which mounts my Dropbox directory:


    def start_mount(mount_dir):
        dropbox_token = os.environ.get('DROPBOX_TOKEN')
        if not os.path.exists(mount_dir):
            os.mkdir(mount_dir)
        subprocess.check_call([sys.executable, 'ff4d.py', mount_dir, '-ap', dropbox_token])


With all of this in place, I'm able to fire up my tornado webapp, and navigate my Dropbox content from within the browser.

The complete code can be found at https://github.com/pelson/heroku-with-dropbox-mount.


### Build & deploy with Docker

Groundwork complete, we now want to put some scaffolding around our proof-of-concept so that we can easily test and deploy
the application on Heroku.

As I mentioned at the beginning, I recently read-up about the new docker based Heroku deployment option, and want to give it a shot.
Since I'm on OSX, I fire up docker-machine (needed an update) and get started with writing my Dockerfile.

I was aware of Continuum's Docker images, and so reached for that as the base image, before extending to my requirements.
There is nothing earth-shattering about the Dockerfile I produced (available at https://github.com/pelson/heroku-with-dropbox-mount),
and my build -> test workflow looks like:

    docker build --tag=docker_webapp_test

and

    docker run -p 5000:5000 -e PORT=5000 -e DROPBOX_TOKEN=<my_token> -t -i docker_webapp_test

As mentioned, I'm using docker-machine to run docker - it essentially manages a VirtualBox machine to run a suitable
host OS for docker. This means that even though the the port was forwarded in my ```docker run``` call, it won't be visible to me on localhost. To find out what IP my machine is running on, we can call ```docker-machine ip <machine_name>```.
It is this address (+":5000") that I use to see the webapp in my browser.

Things are starting to come together nicely, except the mount of my device was failing with messages similar to:

    Starting FUSE...
    fuse: failed to open /dev/fuse: Operation not permitted
    [ERROR] Failed to start FUSE... (Traceback (most recent call last):

It turns out that we need elevated privileges to mount a FUSE device within docker.
Adding ```--cap-add SYS_ADMIN``` and ```--device /dev/fuse``` to docker should be enough (though it appears there was once a bug in docker that meant the container needed to be run with *full* privileges).
I make a note of this as a potential problem for our Heroku deployment.


Finally, I'm able to launch my docker image and navigate my Dropbox content through my web app.
The final step is to push this image to Heroku:

    heroku container:push web

After a considerable amount of time waiting for all of the image layers to upload I get an error in my heroku logs.
Simply changing CMD to something that should obviously work (```ls -ltr```) I get a similar error:

    2017-02-07T11:13:48.755363+00:00 heroku[web.1]: State changed from crashed to starting
    2017-02-07T11:13:56.607038+00:00 heroku[web.1]: Starting process with command `/bin/sh -c \"ls\ -ltr\"`
    2017-02-07T11:13:59.043845+00:00 app[web.1]: Error: No such file or directory

It may be a red-herring, but the command escaping looks a little off.
I iterate further with just ``ls`` as the CMD, but get the same error.
Iterating takes about 30s, so a trial and error approach to solving the problem is proving tedious - I would love to be able to reproduce the issue locally to shorten the loop.
I try removing the quotes within the Dockerfile's CMD section and I ensure that PATH is correctly set - still nothing.

I look back at the docs learn about docker-compose - looks like an interesting tool for managing processes in a similar way to the Proc file within Heroku - definitely something to note for future exploration.

With frustration setting in, I roll back to the Dockerfile provided in the documentation.
This uses alpine as is base and takes some time to upload, but eventually I'm able to confirm that I can at least run CMD on Heroku with that Dockerfile.
Whilst I'd love to understand what is wrong different between Continuum's image and the alpine image (other than the whole OS), my focus on getting my proof-of-concept up and running on Heroku, so I change tactic and update my Dockerfile derive FROM the alpine base image.

After a little more iteration, I eventually manage to use alpine as the base for my webapp's image (including installing ca-certificates to prevent urllib from raising a CERTIFICATE_VERIFY_FAILED exception). I push the image to heroku, and define the DROPBOX_TOKEN environment variable that my code expects in the heroku web portal, but alas there is a problem with the FUSE mount:


    2017-02-07T14:36:06.997268+00:00 app[web.1]: Starting FUSE...
    2017-02-07T14:36:06.997269+00:00 app[web.1]: [ERROR] Failed to start FUSE... (Traceback (most recent call last):
    2017-02-07T14:36:06.997270+00:00 app[web.1]:   File "ff4d/ff4d.py", line 812, in <module>
    2017-02-07T14:36:06.997271+00:00 app[web.1]:     FUSE(Dropbox(ar), mountpoint, foreground=args.background, debug=debug_fuse, sync_read=True, allow_other=allow_other, allow_root=allow_root)
    2017-02-07T14:36:06.997271+00:00 app[web.1]:   File "/opt/webapp/ff4d/fuse.py", line 405, in __init__
    2017-02-07T14:36:06.997272+00:00 app[web.1]:     raise RuntimeError(err)
    2017-02-07T14:36:06.997273+00:00 app[web.1]: RuntimeError: 1

In addition, there is a message in the log along the lines of:

    fuse: device not found, try 'modprobe fuse' first

It may be as I feared: Heroku doesn't currently support FUSE mounts.

In order to get one final datapoint, I put together the equivalent Dockerfile for Ubuntu rather than alpine. Unfortunately the results are the same.

