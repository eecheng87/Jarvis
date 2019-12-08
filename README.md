# Jarvis

[![Generic badge](https://img.shields.io/badge/<Jarvis>-<RELEASED>-<COLOR>.svg)](https://shields.io/)
[![Version](https://img.shields.io/badge/version-v0.0.0-orange.svg)](https://github.com/pytransitions/transitions)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![License](https://img.shields.io/github/license/pytransitions/transitions.svg)](LICENSE)


A personal assistant provide several customize convinient service.

## Setup

### Prerequisite
* Python 3.6
* Pipenv
* HTTPS Server

#### Install Dependency
```sh
pip3 install pipenv

pipenv --three

pipenv install

pipenv shell
```

* pygraphviz (For visualizing Finite State Machine)
    * [Setup pygraphviz on Ubuntu](http://www.jianshu.com/p/a3da7ecc5303)
	* [Note: macOS Install error](https://github.com/pygraphviz/pygraphviz/issues/100)


#### Secret Data
You should generate a `.env` file to set Environment Variables refer to our `.env.sample`.
`LINE_CHANNEL_SECRET` and `LINE_CHANNEL_ACCESS_TOKEN` **MUST** be set to proper values.
Otherwise, you might not be able to run your code.

#### Run Locally
You can either setup https server or using `ngrok` as a proxy.

#### a. Ngrok installation
* [ macOS, Windows, Linux](https://ngrok.com/download)

or you can use Homebrew (MAC)
```sh
brew cask install ngrok
```

**`ngrok` would be used in the following instruction**

```sh
ngrok http 8000
```

After that, `ngrok` would generate a https URL.

#### Run the sever

```sh
python3 app.py
```

## Finite State Machine
![](https://i.imgur.com/MGDr537.png)



## Usage

:memo: Provided Services:

 * Weather report 
  
     :point_right: kaohsiung, tainan, taichung
 * TRA schedule 
  
     :point_right: kaohsiung, tainan, taichung, taipei, hsinchu, jiayi, taoyuan
     
 * PTT
 
     :point_right: Baseball, Beauty
  
   * Check hot post
   * Get image
 

## Commend

:bell: initial state is in `idle`

:bell: all input is case insensitive

:bell: you can type `prev` back to previous state in any case

:bell: you can type `sleep` force jarvis to `idle` in any case 



 * `idle`
     * input `jarvis`
         * enter state `active`
     
 * `active`
     * input `ptt`
         * enter state `ptt`
    * input `weather`
        * enter state `weather`
    * input `train`
        * enter state `train`
*  `ptt`
    *  input `beauty`
        *  enter state `beauty`
    *  input `baseball`
        *  enter state `baseball`
*  `baseball`
    *  feature: show some recommended topic
    *  input: index of topic you want to know more (range is differ in different situation, but start from zero)
    *  next state: `bchoose`
*  `bchoose`
    *  feature: get the link of topic you choose
    *  input: none
    *  next state: `idle`
*  `beauty`
    *  feature: choose the mode you want to enter
    *  input: `popular` (only support one mode now)
    *  next state: `popular`
*  `popular`
    *  feature: enter popular mode and start to acquire image
    *  input: `next` or `np`
    *  next state: `next` or `np`
*   `next`
    *  feature: show next picture in same topic
    *  next state: `popular`
*  `np`
    *  feature: show next picture in next topic
    *  next state: `popular`
* `train`
    * feature: enter your schedule
    * input: {departure}{arrival} {0~23}
        * last query is optional
    * next state: `train_result`
* `train_result`
    * feature: show the all possible ride you can take
    * input: none
    * next state: `idle`
* `weather`
    * feature: ask for location you want to know
    * input: location
    * next state: `degree`
* `degree`
    * feature: show the degree you want to know
    * input: none
    * next state: `idle`
## Unreleased feature
- [ ] search postpone time of train
- [ ] use django
- [ ] add `bus` realtime schedule
## Deploy
Setting to deploy webhooks on Heroku.

### Heroku CLI installation

* [macOS, Windows](https://devcenter.heroku.com/articles/heroku-cli)

or you can use Homebrew (MAC)
```sh
brew tap heroku/brew && brew install heroku
```

or you can use Snap (Ubuntu 16+)
```sh
sudo snap install --classic heroku
```

### Connect to Heroku

1. Register Heroku: https://signup.heroku.com

2. Create Heroku project from website

3. CLI Login

	`heroku login`

### Upload project to Heroku

1. Add local project to Heroku project

	heroku git:remote -a {HEROKU_APP_NAME}

2. Upload project

	```
	git add .
	git commit -m "Add code"
	git push -f heroku master
	```

3. Set Environment - Line Messaging API Secret Keys

	```
	heroku config:set LINE_CHANNEL_SECRET=your_line_channel_secret
	heroku config:set LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
	```

4. Your Project is now running on Heroku!

	url: `{HEROKU_APP_NAME}.herokuapp.com/callback`

	debug command: `heroku logs --tail --app {HEROKU_APP_NAME}`

5. If fail with `pygraphviz` install errors

	run commands below can solve the problems
	```
	heroku buildpacks:set heroku/python
	heroku buildpacks:add --index 1 heroku-community/apt
	```
