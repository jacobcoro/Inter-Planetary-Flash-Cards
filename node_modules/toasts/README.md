#Toasts

Post popups over the page

You might use it in situations where: A query goes wrong, and you want to notify the user. The user has disconnected. The user has received a minor notification.

These situations don't necessarily require any action on the part of the user. Sometimes it's okay for the user to miss the notification altogether if they're not paying attention. But you want the information to be available for those who look. So you post a toast.

see the [demo](http://makopool.com/toasts/demo.html)

##Primary Features

* _Extensively_ configurable. See API

* No dependencies

* As far as the author is aware, Toasts is the only library where toast position changes animate properly as their siblings start to expire. This was acheived through extensive use of fixed positioning. jQuery was not employed, though most toast libraries that use jQuery don't seem to have position animation either. The author really does not understand how people can bring themselves to use such unpolished UIs. Even soundcloud havn't gone to the trouble of animating position changes! The author realizes that the web platform makes this task difficult, but it's worth it, isn't it?! The visual sense is adapted for tracking moving objects! You can't just have things teleporting around the page!


##Example

(did you see the [demo](http://makopool.com/toasts/demo.html) yet?)

```typescript
var Toasts = require('toasts')

var toaster = new Toasts({gravity:[1,1] /*meaning [positive, positive], meaning positioned at the bottom right corner of the screen*/, defaults:{lifespan:Infinity /*= they don't expire. The user has to click on them*/, color:'blue' /*the generation function will be passed the color 'blue'. It might make the background blue. It might just show a blue dot. That's down to the generation function.*/}})
//we haven't specified a generation function though, so the notifications will have the default look. You probably don't want that. You're probably not so lazy or tasteless as to just use whatever is there instead of specifying your own look and structure. In this case you should probably take a look at the generation API below.

toaster.post("watch out")

toaster.post("there's a man behind you")

toaster.post("admittedly quite far away", {color:'black'})
```

##API

```typescript
new Toasts(config)
config: {
	gravity:[number, number] = [1,-1], //(= upper right). a pair of numbers which specify which corner of the screen the toasts will appear in. [-1,1] is left, bottom. [1,1] is right, bottom. You get the idea.
	fadeDuration:number = 200, // the number of milliseconds after a toast's destruction trigger is called, until it is cut from the page. In practical terms: this must be set to the length of your disappearance animations. It's needed to make sure disappearance animations have enough time to complete before removal. 200ms is a good amount, but you can do what you want.
	generationFunction: (msg:string, cfg, invokeDestruction:()=>void)=> {element:HTMLElement, ...}, // the function that generates new toast HTMLElements when Toast.post(msg) is called. Defaults to generating a sort of fadey grey rectangle with rounded corners. Not ideal, for many styles. You'll want another one. Keep reading for simple ways of specifying custom generation functions. Further down is a full explanation of generationFunctions and how to make them
	cssWay: {elementClass, fadeInClass, fadeOutClass}, // using the css way instates a generationFunction that creates a <div class="$elementClass"><span>message</span></div> and uses $fadeInClass and $fadeOutClass to apply fade animations. If you leave out any of the three classes, they'll default to toastbox, toastboxFadingIn, toastboxFadingOut.
	separation: number = 15, //the number of pixels separating toasts from each other and the edges of the screen
	defaults: {lifespan, color} = {lifespan:'suggested', color:'black'} // allows you to set default cfgs for individual toasts. lifespan can be either 'suggested' or the number of milliseconds. 'suggested' determines the lifespan of each post from the length of the message.
}
```
Creates a toaster.



```
Toasts.post(msg:string, cfg = Toasts.defaults):()=>void //posts a toast
```
Toasts. returns a lambda that can be be called to delete the toast.



###Specifying a custom generation function

```typescript
generationFunction: (msg:string, cfg, invokeDestruction:()=>void)=> {
	// `msg` is the message you're to display. `cfg` may contain color and lifespan settings. `invokeDestruction` is a callback you can bind to events to dismiss the toast, once it's been created (if you call it before your generationFunction returns, well, I doubt you have a good reason for doing that, and it wont work out)
	//... your code here ...
	//...
	//... then
	return {
		element, //:HTMLElement. The toast html element that will be displayed
		fadeIn, //:()=>void. optional. A function that will be called immediately after element is added to the page. You can use it to launch fade in animations.
		fadeOut, //:()=>void. optional. A function that will be called shortly before the element is removed from the page. You can use it to launch fade out animations.
		fadeDuration, //:number. optional, defaulting to the toast.fadeDuration of the toaster. The number of milliseconds after fadeOut before the element is removed from the page (allows time for a fade out animation.)
		lifespan //:number. optional, defaulting to toast's global setting.
	}
}
```