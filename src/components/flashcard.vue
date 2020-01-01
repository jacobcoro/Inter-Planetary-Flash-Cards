<template>
    <div id="main">
        <div v-bind:style="{height: height, width: width, backgroundColor: colorFront, color: colorTextFront}" 
        v-show="!isToggle" class="animated flipInY flashcard">
                <p v-bind:style="{fontSize: textSizeFront,fontWeight: 'bold'}">{{front}}</p>
                <img class="img" v-if="imgFront!=''" :src="imgFront">
        </div>
        <div v-bind:style="{height: height, width: width, backgroundColor: colorBack, color: colorTextBack}" 
        v-show="isToggle" class="animated flipInY flashcard">
            <div class="card-content center">
                <p v-bind:style="{fontSize: textSizeBack, fontWeight: 'bold'}">{{back}}</p>
                <img class="img" v-if="imgBack!=''" :src="imgBack">
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
        },
        height: {
              type: String,
            default: '75vw'
        },
        width: {
              type: String,
            default: '90vw'
        }


    }
}
</script>


<style scoped>
.flashcard {
    cursor: pointer;
    border-radius: 10px;
    padding: 25px;
    box-shadow: 0 0px 10px rgba(0, 0, 0, 0.4);
    text-align: left;
    overflow-y: auto;

}

.flashcard:hover {
    box-shadow: 0 0px 25px rgba(0, 0, 0, 0.8);
}

.animated {
    animation-duration:0.8s;
    animation-fill-mode: both;
}

.img {
    object-fit: fill;
    width: 80vw;
    max-height: 60vh;
}

@keyframes flipInY {
    from {
        transform: perspective(300px) rotate3d(0, 1, 0, 90deg);
        animation-timing-function: ease-in;
        opacity: 0;
    }
    40% {
        transform: perspective(300px) rotate3d(0, 1, 0, -20deg);
        animation-timing-function: ease-in;
    }
    60% {
        transform: perspective(300px) rotate3d(0, 1, 0, 10deg);
        opacity: 1;
    }
    80% {
        transform: perspective(300px) rotate3d(0, 1, 0, -5deg);
    }
    to {
        transform: perspective(300px);
    }
}

.flipInY {
    backface-visibility: visible !important;
    animation-name: flipInY;
}
</style>
