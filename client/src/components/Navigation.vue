<script setup>

const props = defineProps({
    link: String,
    msg: String
})
</script>

<template>
    <nav>
        <RouterLink :to="link">
            <span>{{ msg }}</span>
        </RouterLink>
    </nav>
</template>

<style scoped>
nav {
    margin: 2rem 0 2rem;
    padding: 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
nav a {
    text-decoration: none;
    color: black;
    font-size: 1.2rem;
    font-weight: 600;
    display: flex;
    align-items: center;
}

nav span {
    margin-left: .5rem;
}

</style>