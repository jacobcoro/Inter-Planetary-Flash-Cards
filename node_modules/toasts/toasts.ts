
//util
function copyInObject(target, other){
	for(var k in other){
		target[k] = other[k]
	}
	return target
}
function copyObject(v:any){
	var ret = {}
	copyInObject(ret, v)
	return ret
}
function copyInIfNotPresent(target, other){
	for(var  k in other){
		if(target[k] === undefined){
			target[k] = other[k]
		}
	}
	return target
}
function removeArrayItem(ar:any[], i:number){ //if i == -1, does nothing
	if(i >= 0){
		++i
		while(i < ar.length){
			ar[i-1] = ar[i]
			++i
		}
		ar.pop()
	}
}





function positionMessageBoxAlong(v:HTMLElement, along:number, gravity:[number, number]){
	if(gravity[1] > 0){
		v.style.bottom = along+'px'
	}else{
		v.style.top = along+'px'
	}
}
function suggestedLifespanFor(msg:string):number {
	var base = 2500
	var lettersPerSecond = 45/1000
	return base + msg.length/lettersPerSecond
}



type MessageBox = any //expected to contain, element:HTMLElement, fadeOut:()=>void, fadeIn:()=>void, fadeDuration:number
class Toasts{
	defaults = {
		lifespan: 'suggested'
	}
	fadeDuration:number = 200 //milliseconds
	separation:number = 20
	gravity:[number,number] = [1,-1]
	messages:Array<MessageBox> = []
	generate:(msg:string, config:any, invokeDestruction:()=>void)=> any = (msg, config, invokeDestruction)=>{ //creates the html element depending on the message and config. Can be switched out.
		var ret = document.createElement('div')
		ret.style.position = 'absolute'
		ret.style.transition = 'all '+this.fadeDuration+'ms ease-out'
		ret.style.padding = '7px'
		ret.style.margin = '5px'
		ret.style.opacity = '0'
		ret.style.cursor = 'pointer'
		ret.style['min-width'] = '300px'
		ret.style['border-radius'] = '4px'
		ret.style['background-color'] = config.color
		ret.textContent = msg
		ret.addEventListener('click', invokeDestruction)
		return {
			element:ret,
			fadeIn:()=>{ ret.style.opacity = '1' },
			fadeOut:()=>{ ret.style.opacity = '0' }
		}
	}
	constructor(cfg:any = {}){
		if(cfg.generationFunction && cfg.cssWay){
			console.error("toastbox senses that the programmer is confused. There's no reason to give both generationFunction and cssWay. The css way imposes its own toastbox generationFunction, that is its purpose")
		}
		if(cfg.generationFunction){ this.generate = cfg.generationFunction }
		if(cfg.cssWay){
			this.generate = (msg:string, config, invokeDestruction)=> {
				var ret = document.createElement('div')
				ret.classList.add(cfg.cssWay.elementClass || 'toastbox')
				if(config.color) ret.style['background-color'] = config.color
				var tcon = document.createElement('span')
				tcon.textContent = msg
				ret.appendChild(tcon)
				// ret.textContent = msg
				ret.addEventListener('click', invokeDestruction)
				return {
					element:ret,
					fadeIn: ()=>{ ret.classList.add(cfg.cssWay.fadeInClass || 'toastboxFadingIn') },
					fadeOut: ()=>{ ret.classList.add(cfg.cssWay.fadeOutClass || 'toastboxFadingOut') }
				}
			}
		}
		if(cfg.fadeDuration){ this.fadeDuration = cfg.fadeDuration }
		if(cfg.gravity){ this.gravity = cfg.gravity }
		if(cfg.defaults){ copyInObject(this.defaults, cfg.defaults) }
	}
	post(msg:string, config:any = {}):()=>void {
		
		var msgbox:any = {disappearedAlready:false} //this will be completed later, but it needs to be allocated before disappearance is allocated so that it can be captured by reference (and disappearance needs to be made before generate is called, because the generation function needs to be given disappearance, so that it can choose what to bind it to- maybe it wants to bind it to onclick, maybe only to clicking a particular element, maybe not at all. Not for us to decide here)
		
		var disappearance = ()=>{
			if(msgbox.disappearedAlready) return
			msgbox.disappearedAlready = true
			msgbox.fadeOut()
			setTimeout(()=>{
				var i = this.messages.indexOf(msgbox)
				removeArrayItem(this.messages, i)
				//reposition remaining items
				var acc = this.gravity[1] > 0 ?
					msgbox.element.offsetTop + msgbox.element.offsetHeight :
					msgbox.element.offsetTop
				document.body.removeChild(msgbox.element)
				while(i < this.messages.length){
					var tel = this.messages[i].element
					positionMessageBoxAlong(tel, acc, this.gravity)
					acc += this.separation + tel.offsetHeight
					++i
				}
				
				//reduce potential for leaks if user accidentally holds onto a ref of disappearance
				for(var k in msgbox){
					msgbox[k] = undefined
				}
				msgbox.disappearedAlready = true
			}, msgbox.fadeDuration)
		}
		
		var cfg = copyInObject(copyObject(this.defaults), config)
		var generata = this.generate(msg, cfg, disappearance)
		copyInIfNotPresent(
			copyInObject(msgbox, generata),
			{
				fadeDuration:this.fadeDuration,
				fadeIn: ()=>{},
				fadeOut: ()=>{},
				lifespan: cfg.lifespan
			}
		)
		var endMsgbox = this.messages.length ? this.messages[this.messages.length-1] : null
		var after = endMsgbox&&endMsgbox.element
		if(this.gravity[0] == -1){
			msgbox.element.style.left = this.separation+'px'
		}else if(this.gravity[0] == 1){
			msgbox.element.style.right = this.separation+'px' }
		if(this.gravity[1] == -1){
			msgbox.element.style.top = this.separation + (after ? after.offsetTop + after.offsetHeight : 0) + 'px'
		}else if(this.gravity[1] == 1){
			msgbox.element.style.bottom = this.separation + (after ? after.offsetLeft : 0) + 'px'
		}
		document.body.appendChild(msgbox.element)
		this.messages.push(msgbox)
		setTimeout(msgbox.fadeIn, 16) //wont animate if we do it right away
		
		if(msgbox.lifespan != Infinity){
			var lifespan = (msgbox.lifespan == 'suggested')?
				suggestedLifespanFor(msg) :
				msgbox.lifespan
			setTimeout(disappearance, lifespan)
		}
		
		return disappearance
	}
}


export = Toasts