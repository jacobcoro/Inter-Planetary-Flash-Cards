<template>
    <div>
        <div v-bind:style="{backgroundColor: colorFront, color: colorTextFront}" 
        v-show="!isToggle" class="animated flipInY flashcard">
            <div class="card-content center">
                <p v-bind:style="{fontSize: textSizeFront,fontWeight: 'bold'}">{{front}}</p>
                <img v-if="imgFront!=''" :src="imgFront" width="350" height="200">
            </div>
        </div>
        <div v-bind:style="{backgroundColor: colorBack, color: colorTextBack}" 
        v-show="isToggle" class="animated flipInY flashcard">
            <div class="card-content center">
                <p v-bind:style="{fontSize: textSizeBack, fontWeight: 'bold'}">{{back}}</p>
                <!-- need to change this to resize photo based on original but with a max -->
                <img v-if="imgBack!=''" :src="imgBack" width="350" height="200">
            </div>
        </div>
    </div>
</template>
<script>
export default {
    data() {
        return {
            
        }
    }, props: {
        imgFront: {
            type: String,
            default: ''
        },
        imgBack: {
            type: String,
            default: ''
        },
        front: {
            type: String,
            default: ''
        },
        back: {
            type: String,
            default: ''
        },
        textSizeFront: {
            type: String,
            default: '1.5em'
        },
        textSizeBack: {
            type: String,
            default: '1.5em'
        },
        colorTextFront: {
            type: String,
            default: 'black'
        },
        colorTextBack: {
            type: String,
            default: 'black'
        },
        colorFront: {
            type: String,
            default: 'white'
        },
        colorBack: {
            type: String,
            default: 'white'
        },
        isToggle: {
            type: Boolean,
            // default: false
        }


    }
}
</script>


<style scoped>
.center {
    text-align: center;
}

.flashcard {
    cursor: pointer;
    border-radius: 10px;
    width: 400px;
    height: 500px;
    margin: 20px;
    padding: 25px;
    box-shadow: 0 0px 10px rgba(0, 0, 0, 0.4);
    text-align: left;
}

.flashcard:hover {
    box-shadow: 0 0px 25px rgba(0, 0, 0, 0.8);
}

.animated {
    animation-duration: 1s;
    animation-fill-mode: both;
}

@keyframes flipInY {
    from {
        transform: perspective(400px) rotate3d(0, 1, 0, 90deg);
        animation-timing-function: ease-in;
        opacity: 0;
    }
    40% {
        transform: perspective(400px) rotate3d(0, 1, 0, -20deg);
        animation-timing-function: ease-in;
    }
    60% {
        transform: perspective(400px) rotate3d(0, 1, 0, 10deg);
        opacity: 1;
    }
    80% {
        transform: perspective(400px) rotate3d(0, 1, 0, -5deg);
    }
    to {
        transform: perspective(400px);
    }
}

.flipInY {
    backface-visibility: visible !important;
    animation-name: flipInY;
}
</style>
