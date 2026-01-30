<template>
    <div class="container py-4">
        <h3>Login</h3>
        <div class="mb-2">
            <input v-model="username" class="form-control" placeholder="username" />
        </div>
        <div class="mb-2">
            <input type="password" v-model="password" class="form-control" placeholder="password" />
        </div>
        <button class="btn btn-primary" @click="doLogin">Login</button>
        <div v-if="error" class="text-danger mt-2">{{ error }}</div>
    </div>
</template>

<script>
import { login } from "../services/auth";

export default {
    data(){
        return { username: "", password: "", error: null };
    },

    methods: {
        async doLogin() {
            this.error = null;
            try{
                await login(this.username, this.password);
                this.$emit("login-success");
            } catch (err) {
                this.error = err.detail || JSON.stringify(err);
            }
        },
    },
};

</script>