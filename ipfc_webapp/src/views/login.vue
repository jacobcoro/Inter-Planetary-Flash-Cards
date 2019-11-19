<template>
    <div id="login">
        <h1>Login</h1>
        <input type="text" name="username" v-model="input.username" placeholder="Username" />
        <input type="password" name="password" v-model="input.password" placeholder="Password" />
        <input type="text" name="server" v-model="input.server" placeholder="Server" data-value="https://ipfc-midware.herokuapp.com/" readonly/>
        <button type="button" v-on:click="login()">Login</button>

              <ul v-if="errors && errors.length">
            <li v-for="error of errors" v-bind:key="error" >
            {{error.message}}
            </li>
        </ul>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: 'Login',
        data() {
            return {
                errors: [],
                input: {
                    username: "",
                    password: "",
                    server: ""
                }
            }
        },
        methods: {

            login() {
                let server = "https://ipfc-midware.herokuapp.com/";
                console.log("Posting to "+ this.input.server);
                //from https://alligator.io/vuejs/rest-api-axios/
                let authReq = {
                    'user': this.input.username,
                    'password': this.input.password
                }
                axios.post(server, {
                    body: authReq
                })
                .then(response => {
                    console.log(response);
                })
                .catch(e => {
                    this.errors.push(e)
                })


                /*try {
                    await axios.post(this.input.server, {
                          body: this.postBody
                    })
                } catch (e) {
                   this.errors.push(e)
                }
                */

                /**if(this.input.username != "" && this.input.password != "") {
                    if(this.input.username == this.$parent.mockAccount.username && this.input.password == this.$parent.mockAccount.password) {
                        this.$emit("authenticated", true);
                        this.$router.replace({ name: "secure" });
                    } else {
                        console.log("The username and / or password is incorrect");
                    }
                } else {
                    console.log("A username and password must be present");
                }*/
            }
        }
    }
</script>

<style scoped>
    #login {
        width: 500px;
        border: 1px solid #CCCCCC;
        background-color: #FFFFFF;
        margin: auto;
        margin-top: 200px;
        padding: 20px;
    }
</style>