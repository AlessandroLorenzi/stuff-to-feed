# STUFF TO FEED

Transform stuff to feed rss

## The "stuff" supported

### RAI Program

Use the name of the program from the url and use it as slug (eg: for `https://www.raiplaysound.it/programmi/ungiornodapecora` use `ungiornodapecora`)

* `https://stufftofeed.alorenzi.eu/rai/<slug>`

### Telegram channel

Use the name of the channel from the url and use it as slug (eg: for `https://t.me/ultimora` use `ultimora`)

* `https://stufftofeed.alorenzi.eu/telegram/<slug>`

## Setup

1. Clone the repo in `/srv` 
2. Create an app in https://my.telegram.org 
3. Copy the `envrc.example` in `.envrc` and set secrets
4. Create the systemd service with `systemctl edit --full --force stufftofeed.service` and copy the (stuff-to-feed.service)[doc/stuff-to-feed.service] content. Adapt if needed.
5. `systemctl enable --now stufftofeed.service`

At first telegram call it will create a telegram session. It will ask you for a phone name and will send you a code. (**TODO**: improve this part of documentation, maybe need to create a script to pre-generate the session file).
