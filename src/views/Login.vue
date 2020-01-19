
<template>
<div id="body">
    <b-alert
      :show="dismissCountDown"
      dismissible
      fade
      variant="warning"
      @dismiss-count-down="countDownChanged"
    >
    {{ apiErrorMsg }}
    </b-alert>
    <h1>IPFC Login</h1>
    <b-form @submit.stop.prevent id="form-signin">
        <label for="feedback-email">Email</label>
        <b-input v-model="input.email" :state="emailValidation" id="feedback-email"></b-input>
        <b-form-invalid-feedback v-if="input.email" :state="emailValidation">{{ emailValidationErrorMsg }}</b-form-invalid-feedback>
        <!-- <b-form-valid-feedback :state="emailValidation">Looks Good.</b-form-valid-feedback> -->
        
        <label for="feedback-password">Password</label>
        <b-input v-model="input.password" :state="passwordValidation" type="password" id="feedback-password"></b-input>
        <b-form-invalid-feedback v-if="input.password" :state="passwordValidation">{{ passwordValidationErrorMsg }}</b-form-invalid-feedback>
        <!-- <b-form-valid-feedback :state="passwordValidation">Looks Good.</b-form-valid-feedback> -->
        
        <b-button v-if="signingUp" id="button-get-pinata" type="submit" @click="OpenPinata()" variant="primary">Get Pinata</b-button>
        <br>
        
        <label v-if="signingUp" for="feedback-pinata-api">Pinata API key</label>
        <b-input v-if="signingUp" v-model="input.pinataApi" :state="pinataApiValidation" id="feedback-pinata-api"></b-input>
        <b-form-invalid-feedback v-if="signingUp" :state="pinataApiValidation">{{ pinataApiValidationErrorMsg }}</b-form-invalid-feedback>
        <!-- <b-form-valid-feedback v-if="signingUp" :state="pinataApiValidation">Looks Good.</b-form-valid-feedback> -->
       
        <label v-if="signingUp" for="feedback-pinata-secret">Pinata secret API key</label>
        <b-input v-if="signingUp" v-model="input.pinataSecret" :state="pinataSecretValidation" type="password" id="feedback-pinata-secret"></b-input>
        <b-form-invalid-feedback v-if="signingUp" :state="pinataSecretValidation">{{ pinataSecretValidationErrorMsg }}</b-form-invalid-feedback>
        <!-- <b-form-valid-feedback v-if="signingUp" :state="pinataSecretValidation">Looks Good.</b-form-valid-feedback> -->
        
        <span id="login-signup-buttons">
            <b-button v-if="signingUp" :disabled="loginButtonDisable" type="submit" @click="SignUp()" variant="primary">
                <font-awesome-icon v-show="loggingIn" icon="spinner" spin />
                Sign up</b-button>
            <b-button v-else :disabled="loginButtonDisable" type="submit" @click="login()" variant="primary">
                <font-awesome-icon v-show="loggingIn" icon="spinner" spin />
                Log in</b-button>
            
            <b-button v-if="signingUp" :disabled="loginButtonDisable" type="submit" id="sign-up-a" @click="toggleSigningUp()" variant="secondary">Log in</b-button>
            <b-button v-else :disabled="loginButtonDisable" type="submit" id="sign-up-a" @click="toggleSigningUp()" variant="secondary">Sign up</b-button>
        </span>
    </b-form>
</div>
</template>
<script>
import { mapState } from 'vuex'

export default {
    name: 'Login',
    data() {
        return {
            input: {
                email: '',
                password: '',
                pinataApi: '',
                pinataSecret: ''
            },
            apiErrorMsg: '',
            failedLogin: false,
            dismissSecs: 5,
            dismissCountDown: 0,
            loggingIn: false,
            signingUp: false
        }
    },
    computed: {
        ...mapState({
           serverURL: 'serverURL'
        }),
        emailValidation () {
            let email = this.input.email
            if (email.length < 4 || email.length > 25) {
                return false
            }
            if (!email.includes('@') || !email.includes('.')) {
                return false
            }
            else {
                return true
            }            
        },
        emailValidationErrorMsg () {
            let email = this.input.email
            if (email.length < 4 || email.length > 25) {
                return "Email must be 5-25 characters long"
            }
            if (!email.includes('@') || !email.includes('.')) {
                return "Invalid email"
            }
             else {
                return null
            }    
        },
        passwordValidation () {
            let password = this.input.password
            if (password.length < 8 || password.length > 20) {
                return false
            }
            else {
                return true
            }            
        },
        passwordValidationErrorMsg () {
            let password = this.input.password
            if (password.length < 8 || password.length > 20) {
                return "Password must be 8-20 characters long"
            }
             else {
                return null
            }    
        },
        pinataApiValidation () {
            let pinataApi = this.input.pinataApi
            if (pinataApi.length < 20 || pinataApi.length > 20) {
                return false
            }
            else {
                return true
            }            
        },
        pinataApiValidationErrorMsg () {
            let pinataApi = this.input.pinataApi
            if (pinataApi.length < 20 || pinataApi.length > 20) {
                return "Invalid pinata api key. In pinata, click the profile icon, then 'account'"
            }
             else {
                return null
            }    
        },
        pinataSecretValidation () {
            let pinataSecret = this.input.pinataSecret
            if (pinataSecret.length < 64 || pinataSecret.password > 64) {
                return false
            }
            else {
                return true
            }            
        },
        pinataSecretValidationErrorMsg () {
            let pinataSecret = this.input.pinataSecret
            if (pinataSecret.length < 64 || pinataSecret.length > 64) {
                return "Invalid pinata api secret key. In pinata, click the profile icon, then 'account'"
            }
             else {
                return null
            }
        },
        invalidSignUp () {
           if (!this.emailValidation || !this.passwordValidation || !this.pinataApiValidation || !this.pinataSecretValidation) {
               return true
           }else {
               return false
           }
        },
        invalidLogin () {
           if (!this.emailValidation || !this.passwordValidation) {
               return true
           }else {
               return false
           }
        },
        loginButtonDisable () {
            if (!this.emailValidation || !this.passwordValidation || this.loggingIn) {
               return true
           }else {
               return false
           }
        }

    },
    watch: {
        failedLogin: function () {
            if (this.failedLogin === true) {
                this.showAlert()
            }   
        }
    },
    methods: {
        login () {
            this.loggingIn = true
            this.failedLogin = false
            let loginURL = this.serverURL + "/login";
            let headers = new Headers();
            let username = this.input.email;
            let password = this.input.password;
            headers.append('Content-Type', 'application/json');
            headers.append('Authorization', 'Basic ' + btoa(username + ":" + password));                            
            fetch(loginURL, { headers: headers })
                .then(response => response.json())
                .then((data) => {
                    // console.log(data);
                    if (!data['token']) {
                        this.failedLogin = true
                        this.apiErrorMsg = data['error']
                    }
                    else {
                        this.$store.commit('updateJwt', data['token']);
                        this.$store.dispatch('checkJwt')
                        this.$store.commit('updateUserCollection', data['user_collection'])
                        this.$store.commit('updateDecksMeta', data['decks_meta'])
                        this.$store.commit('updateDecks', data['decks'])
                        this.$store.dispatch('refreshLastSyncsData')
                        this.$router.push('home');
                    }
                    this.loggingIn = false
                    })
                    .catch(function() {
                        //console.log(error);
                        // this returns an error
                        this.failedLogin = true
                        this.apiErrorMsg = 'Server error'
                    });
                    
        },
        SignUp () {
            this.loggingIn = true
            this.failedLogin = false
            let signupURL = this.serverURL + "/sign_up";
            let data = {
                'email': this.input.email,
                'password': this.input.password,
                'pinata_api': this.input.pinataApi,
                'pinata_key': this.input.pinataSecret
            }
            fetch(signupURL, { 
                headers: { 'Content-Type': 'application/json'},
                body: JSON.stringify(data),
                method: 'POST',
                })
                .then(response => response.json())
                .then((data) => {
                    // console.log(data);
                    if (!data['message']) {
                        this.failedLogin = true
                        this.apiErrorMsg = data['error']
                    }
                    else {
                        this.login ();
                    }
                    this.loggingIn = false
                    }).catch(function() {
                        this.failedLogin = true
                        this.apiErrorMsg = 'Server error'
                        //console.log(error);
                    });
            
        },
        toggleSigningUp () {
            this.signingUp = !this.signingUp
        },
        changeErrorMsg (msg) {
            this.emailValidationErrorMsg = msg
        },
        OpenPinata () {
            window.open("https://pinata.cloud/signup", "_blank")
        },
        countDownChanged(dismissCountDown) {
        this.dismissCountDown = dismissCountDown
        },
        showAlert() {
        this.dismissCountDown = this.dismissSecs
        }
    }
}

</script>

<style scoped>
#body {
    padding: 20px;
}
#form-signin {
    max-width: 330px;
}
#sign-up-a {
    margin: 10px;
}
#login-signup-buttons{
    margin-top: 10px;
}
#button-get-pinata {
    margin-top: 10px;
}
label {
    margin-top: 5px;
}
</style>    