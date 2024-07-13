# Watcom Docker Build Environment

Forked from [crempp/watcom-docker](https://github.com/crempp/watcom-docker) which has not been updated in years.
The original docker image pulled the latest sources and built Open Watcom V2 in the image.
This version uses the pre-built snapshot to build a docker image tagged with the release it came from.
I primarily created this as a means to build [arlaneenalra/xta2sd-active-boot](https://github.com/arlaneenalra/xta2sd-active-boot) locally without having to install Open Watcom V2 on my system directly. 

The image is based on Alpine 3.20 and includes:
* make
* xxd - A hex dumping and reversing tool.
* nasm - The Netwide Assembler.

# Using the Image

To run in an interactive mode:
```
$ docker run -it -v $(pwd):/src ghcr.io/arlaneenalra/watcom-docker sh 
```

or

```
$ docker run -it -v $(pwd):/src arlaneenalra/watcom-docker sh 
```

To build something:
```
$ echo -e '#include <stdio.h>\nvoid main() { printf("Hello World\\n"); }' > hello.c
$ docker run --rm -v $(pwd):/src ghcr.io/arlaneenalra/watcom-docker wcl hello.c 

or 

$ docker run --rm -v $(pwd):/src arlaneenalra/watcom-docker wcl hello.c 
```

# Building the Image Locally

## To Build the Current-build Version.
```
$ docker build . -t <tag> 
```

## To Build and Arbitrary Release Tag
Pick a release tag from [open-watcom/open-watcom-v2](https://github.com/open-watcom/open-watcom-v2/tags).

Example building 2024-07-05-Build.
```
$ docker build --build-arg RELEASE=2024-07-05-Build . -t <tag> 
```


