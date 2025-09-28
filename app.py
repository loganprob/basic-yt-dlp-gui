from flask import (
    Flask, 
    render_template, 
    send_from_directory, 
    make_response,
    request)
import os
import re
from yt_dlp import YoutubeDL


def parse_url(url:str) -> dict|None:
    parsed = re.fullmatch(r'(?P<core_url>.+youtube.com/watch\?v=(?P<video_id>[^&]+)).*', url)
    if parsed:
        return parsed.groupdict()
    return


def _get_preset_params(preset:str):
    match preset:
        case 'mp3':
            return {
                'format': 'ba[acodec^=mp3]/ba/b',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                }]
            }
        case 'mp4':
            return {
                'format': 'bv+ba/b',
                'merge_output_format': 'mp4',
                'remux_video': 'mp4',
                'postprocessors': [{
                    'key': 'FFmpegVideoRemuxer',
                    'preferedformat': 'mp4',
                }],
                'sort': ['vcodec:h264', 'lang', 'quality', 'res', 'fps', 'hdr:12', 'acodec:aac']
            }
        case _:
            raise ValueError(f"Unsupported preset: {preset}")


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/reset-form')
def reset_form():
    return render_template('form-reset.html')


@app.route('/download/<filename>')
def download(filename:str):
    return send_from_directory('downloads', filename, as_attachment=True)


@app.route('/get-thumbnail')
def get_thumbnail():
    thumbnail_url = None
    video_url = request.args.get('video-url','').strip()
    if video_url and (parsed_url:=parse_url(video_url)):
        video_id = parsed_url['video_id']
        thumbnail_url = video_id
    
    # format: https://stackoverflow.com/questions/2068344/how-do-i-get-a-youtube-video-thumbnail-from-the-youtube-api

    response = make_response(render_template('thumbnail-preview.html', thumbnail_url=thumbnail_url))
    response.headers['HX-Retarget'] = '#thumbnail-preview'
    response.headers['HX-Reswap'] = 'innerHTML'
    return response


@app.route('/get-video')
def get_video():
    response = make_response()

    video_url = request.args.get('video-url','').strip()
    if not video_url or not (parsed_url:=parse_url(video_url)):
        response.headers['HX-Retarget'] = '#error-alert'
        response.headers['HX-Trigger'] = 'form-errors'
        response.headers['HX-Reswap'] = 'none'
        return response
    
    request_url = parsed_url['core_url']
    params = _get_preset_params(request.args.get('output-preset'))
    params['outtmpl'] = f'downloads/{request.args.get('rename-file') or '%(title)s'}.%(ext)s'

    # not sure how to get the actual file name if not renamed, 
    # before/after comparison is a janky workaround
    before_files = set(os.listdir('downloads'))

    with YoutubeDL(params) as ydl:
        ydl.download([request_url])

    after_files = set(os.listdir('downloads'))
    diff_file = list(after_files - before_files)[0]

    response.headers['HX-Redirect'] = f'/download/{diff_file}'
    response.headers['HX-Trigger'] = 'reset-form'
    return response




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)