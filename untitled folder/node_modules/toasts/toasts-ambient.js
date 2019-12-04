this["Toasts"] =
/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};

/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {

/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId])
/******/ 			return installedModules[moduleId].exports;

/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			exports: {},
/******/ 			id: moduleId,
/******/ 			loaded: false
/******/ 		};

/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);

/******/ 		// Flag the module as loaded
/******/ 		module.loaded = true;

/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}


/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;

/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;

/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";

/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ function(module, exports) {

	"use strict";
	//util
	function copyInObject(target, other) {
	    for (var k in other) {
	        target[k] = other[k];
	    }
	    return target;
	}
	function copyObject(v) {
	    var ret = {};
	    copyInObject(ret, v);
	    return ret;
	}
	function copyInIfNotPresent(target, other) {
	    for (var k in other) {
	        if (target[k] === undefined) {
	            target[k] = other[k];
	        }
	    }
	    return target;
	}
	function removeArrayItem(ar, i) {
	    if (i >= 0) {
	        ++i;
	        while (i < ar.length) {
	            ar[i - 1] = ar[i];
	            ++i;
	        }
	        ar.pop();
	    }
	}
	function positionMessageBoxAlong(v, along, gravity) {
	    if (gravity[1] > 0) {
	        v.style.bottom = along + 'px';
	    }
	    else {
	        v.style.top = along + 'px';
	    }
	}
	function suggestedLifespanFor(msg) {
	    var base = 2500;
	    var lettersPerSecond = 45 / 1000;
	    return base + msg.length / lettersPerSecond;
	}
	var Toasts = (function () {
	    function Toasts(cfg) {
	        var _this = this;
	        if (cfg === void 0) { cfg = {}; }
	        this.defaults = {
	            lifespan: 'suggested'
	        };
	        this.fadeDuration = 200; //milliseconds
	        this.separation = 20;
	        this.gravity = [1, -1];
	        this.messages = [];
	        this.generate = function (msg, config, invokeDestruction) {
	            var ret = document.createElement('div');
	            ret.style.position = 'absolute';
	            ret.style.transition = 'all ' + _this.fadeDuration + 'ms ease-out';
	            ret.style.padding = '7px';
	            ret.style.margin = '5px';
	            ret.style.opacity = '0';
	            ret.style.cursor = 'pointer';
	            ret.style['min-width'] = '300px';
	            ret.style['border-radius'] = '4px';
	            ret.style['background-color'] = config.color;
	            ret.textContent = msg;
	            ret.addEventListener('click', invokeDestruction);
	            return {
	                element: ret,
	                fadeIn: function () { ret.style.opacity = '1'; },
	                fadeOut: function () { ret.style.opacity = '0'; }
	            };
	        };
	        if (cfg.generationFunction && cfg.cssWay) {
	            console.error("toastbox senses that the programmer is confused. There's no reason to give both generationFunction and cssWay. The css way imposes its own toastbox generationFunction, that is its purpose");
	        }
	        if (cfg.generationFunction) {
	            this.generate = cfg.generationFunction;
	        }
	        if (cfg.cssWay) {
	            this.generate = function (msg, config, invokeDestruction) {
	                var ret = document.createElement('div');
	                ret.classList.add(cfg.cssWay.elementClass || 'toastbox');
	                if (config.color)
	                    ret.style['background-color'] = config.color;
	                var tcon = document.createElement('span');
	                tcon.textContent = msg;
	                ret.appendChild(tcon);
	                // ret.textContent = msg
	                ret.addEventListener('click', invokeDestruction);
	                return {
	                    element: ret,
	                    fadeIn: function () { ret.classList.add(cfg.cssWay.fadeInClass || 'toastboxFadingIn'); },
	                    fadeOut: function () { ret.classList.add(cfg.cssWay.fadeOutClass || 'toastboxFadingOut'); }
	                };
	            };
	        }
	        if (cfg.fadeDuration) {
	            this.fadeDuration = cfg.fadeDuration;
	        }
	        if (cfg.gravity) {
	            this.gravity = cfg.gravity;
	        }
	        if (cfg.defaults) {
	            copyInObject(this.defaults, cfg.defaults);
	        }
	    }
	    Toasts.prototype.post = function (msg, config) {
	        var _this = this;
	        if (config === void 0) { config = {}; }
	        var msgbox = { disappearedAlready: false }; //this will be completed later, but it needs to be allocated before disappearance is allocated so that it can be captured by reference (and disappearance needs to be made before generate is called, because the generation function needs to be given disappearance, so that it can choose what to bind it to- maybe it wants to bind it to onclick, maybe only to clicking a particular element, maybe not at all. Not for us to decide here)
	        var disappearance = function () {
	            if (msgbox.disappearedAlready)
	                return;
	            msgbox.disappearedAlready = true;
	            msgbox.fadeOut();
	            setTimeout(function () {
	                var i = _this.messages.indexOf(msgbox);
	                removeArrayItem(_this.messages, i);
	                //reposition remaining items
	                var acc = _this.gravity[1] > 0 ?
	                    msgbox.element.offsetTop + msgbox.element.offsetHeight :
	                    msgbox.element.offsetTop;
	                document.body.removeChild(msgbox.element);
	                while (i < _this.messages.length) {
	                    var tel = _this.messages[i].element;
	                    positionMessageBoxAlong(tel, acc, _this.gravity);
	                    acc += _this.separation + tel.offsetHeight;
	                    ++i;
	                }
	                //reduce potential for leaks if user accidentally holds onto a ref of disappearance
	                for (var k in msgbox) {
	                    msgbox[k] = undefined;
	                }
	                msgbox.disappearedAlready = true;
	            }, msgbox.fadeDuration);
	        };
	        var cfg = copyInObject(copyObject(this.defaults), config);
	        var generata = this.generate(msg, cfg, disappearance);
	        copyInIfNotPresent(copyInObject(msgbox, generata), {
	            fadeDuration: this.fadeDuration,
	            fadeIn: function () { },
	            fadeOut: function () { },
	            lifespan: cfg.lifespan
	        });
	        var endMsgbox = this.messages.length ? this.messages[this.messages.length - 1] : null;
	        var after = endMsgbox && endMsgbox.element;
	        if (this.gravity[0] == -1) {
	            msgbox.element.style.left = this.separation + 'px';
	        }
	        else if (this.gravity[0] == 1) {
	            msgbox.element.style.right = this.separation + 'px';
	        }
	        if (this.gravity[1] == -1) {
	            msgbox.element.style.top = this.separation + (after ? after.offsetTop + after.offsetHeight : 0) + 'px';
	        }
	        else if (this.gravity[1] == 1) {
	            msgbox.element.style.bottom = this.separation + (after ? after.offsetLeft : 0) + 'px';
	        }
	        document.body.appendChild(msgbox.element);
	        this.messages.push(msgbox);
	        setTimeout(msgbox.fadeIn, 16); //wont animate if we do it right away
	        if (msgbox.lifespan != Infinity) {
	            var lifespan = (msgbox.lifespan == 'suggested') ?
	                suggestedLifespanFor(msg) :
	                msgbox.lifespan;
	            setTimeout(disappearance, lifespan);
	        }
	        return disappearance;
	    };
	    return Toasts;
	}());
	module.exports = Toasts;


/***/ }
/******/ ]);