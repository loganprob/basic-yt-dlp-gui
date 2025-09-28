# basic-yt-dlp-gui

It... works. 

Very limited wrapper around [yt-dlp](https://github.com/yt-dlp/yt-dlp) to run in the browser via docker container. Only supports the standard mp3 and mp4 presets right now. Very rough, no error handling, one-night project.

## Install
> [!IMPORTANT] 
> Assumes you already have [Git](https://git-scm.com/downloads) and [Docker](https://docs.docker.com/engine/install/) installed.

1. Clone Github repo
    ```
    git clone https://github.com/loganprob/basic-yt-dlp-gui.git
    ```

2. Navigate into newly cloned directory
    ```
    cd basic-yt-dlp-gui
    ```

3. Build Docker image and run the container
    ```
    docker compose up --build -d
    ```

4. Once container is running, open [http://localhost:8080] in browser

Container is now live and running in the background. You can create a bookmark for the address to easily navigate back.

To shut down the docker container:

```
docker compose down
```

## To Do

- [X] Option to rename the generated file name when saving
- [ ] Error handling, across the board :(
- [ ] Non UTF-8 characters in file names prevent saving (during the re-read step, not the downloading step)
- [ ] CSS styling
- [ ] Drag and drop support
- [ ] Thumbnail previews before download
- [ ] Loading indicator, some way to communicate download progress
- [ ] Sometimes mp3's will download as webm's?