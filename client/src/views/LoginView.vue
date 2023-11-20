<script setup>
import { ref } from 'vue'
import router from '../router'
import { store } from '../store/store'
import { api } from '../store/api'

const username = ref(null)
const password = ref(null)

async function signin() {
    const response = await api.authenticate(username.value, password.value)
    if (!response.ok) {
        console.log("An error occured during authentication!")
        api.test()
        return
    }

    const responseJson = await response.json()
    const token = responseJson.access_token
    if (token) {
        store.isLoggedIn = true
        store.accessToken = token
        router.push({name: 'home'})
    }
}

async function signup() {
    const response = await api.register(username.value, password.value)
    if (!response.ok) {
        console.log("An error occured during registration!")
        return
    }
}
</script>

<template>
        <main>
        <input v-model="username" placeholder="Username">
        <input v-model="password" placeholder="Password" type="password" >
        <section>
            <button @click.stop="signup">Register</button>
            <button @click.stop="signin">Sign in</button>
        </section>
    </main>
</template>

<style scoped>
main {
    margin: 1rem;
    padding: 1.5rem;
    background-color: var(--clr-background-main);
    color: #232c3b;
    border-radius: 1.25rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

input {
    height: 2rem;
    width: 250px;
    margin: 5px;
    outline: none;
    border-radius: 5px;
    border: 1px solid lightgrey;
}

section {
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>
