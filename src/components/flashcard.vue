<template>
    <div id="main">
        <div v-bind:style="{ backgroundColor: colorFront, color: colorTextFront}" 
        v-show="!isToggle" class="animated flipInY flashcard">
            <div class="card-content">
                <p v-bind:style="{fontSize: textSizeFront,fontWeight: 'bold'}">{{front}}</p>
                <img class="img" v-if="imgFront!=''" :src="imgFront">
            </div>
        </div>
        <div v-bind:style="{backgroundColor: colorBack, color: colorTextBack}" 
        v-show="isToggle" class="animated flipInY flashcard">
            <div class="card-content">
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
    },
    computed: {
        textSizeFront () {
            if (this.front.length < 20) {
                return '4em'
            }
            else if (this.front.length < 50) {
                return '3em'
            }
            else if (this.front.length < 250) {
                return '2em'
            }
            else if (this.front.length < 350) {
                return '1.5em'
            }
            else return '1em'
        },
        textSizeBack () {
            if (this.back.length < 20) {
                return '4em'
            }
            else if (this.back.length < 50) {
                return '3em'
            }
            else if (this.back.length < 250) {
                return '2em'
            }
            else if (this.back.length < 350) {
                return '1.5em'
            }
            else return '1em'
        }
    }, 
    props: {
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
        // textSizeFront: {
        //     type: String,
        //     default: '1.5em'
        // },
        // textSizeBack: {
        //     type: String,
        //     default: '1.5em'
        // },
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
        },
        // height: {
        //       type: String,
        //     default: '60vh'
        // },
        // width: {
        //       type: String,
        //     default: '90vw'
        // }
    }
}
</script>


<style scoped>
/* #main {
    background-color: rgba(0, 0, 0, 0);
        border-radius: 10px;

} */
.flashcard {
    align-content: center;
    justify-content: center;
    cursor: pointer;
    border-radius: 10px;
    box-shadow: 0 0px 10px rgba(0, 0, 0, 0.4);
    height: calc(100vh - 180px);
    margin: auto;
    width: 100%;
    padding: 0px 10px 0px 20px;
}
.flashcard:hover {
    box-shadow: 0 0px 25px rgba(0, 0, 0, 0.8);
}
/* this brings the scroll bar into the card so its not creating a square corner */
.card-content {
    padding: 10px 10px 0px 0px;
    margin: auto;
    height: 100%;
    overflow-y: auto;
}
.card-content::-webkit-scrollbar {
    width: .5em;
}
.card-content::-webkit-scrollbar-thumb {
    background-color: lightgrey;
    border-radius: 5px;
}
.animated {
    animation-duration:.65s;
    animation-fill-mode: both;
}
.img {
    object-fit: fill;
    width: 100%;
    margin: auto;
}

@keyframes flipInY {
    from {
        transform: perspective(300px) rotate3d(0, 1, 0, 90deg);
        animation-timing-function: ease-in;
        opacity: .97;
    }
    40% {
        transform: perspective(300px) rotate3d(0, 1, 0, -10deg);
        animation-timing-function: ease-in;
    }
    60% {
        transform: perspective(300px) rotate3d(0, 1, 0, 5deg);
        opacity: 1;
    }
    80% {
        transform: perspective(300px) rotate3d(0, 1, 0, -2deg);
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
