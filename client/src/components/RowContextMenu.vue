<script setup>
import { ref } from 'vue';
import IconDotsHorizontalRounded from './icons/IconDotsHorizontalRounded.vue';

const props = defineProps({
    actions: Array
})

const emit = defineEmits(['actionClick'])

const isContextMenuShown = ref(false)

function showContextMenu() {
    isContextMenuShown.value = true
}

function closeContextMenu() {
    isContextMenuShown.value = false
}

function onMenuItemClick(actionName) {
    isContextMenuShown.value = false
    emit('actionClick', actionName)
}
</script>

<template>
    <div style="position: relative;">
        <IconDotsHorizontalRounded @click.stop="showContextMenu" />
        <div v-if="isContextMenuShown" class="click-intercept" @click.stop="closeContextMenu"></div>
        <ul v-if="isContextMenuShown" class="context">
            <li v-for="action in props.actions" @click.stop="() => onMenuItemClick(action.name)">
                {{ action.text }}
            </li>
        </ul>
    </div>
</template>

<style scoped>
.click-intercept {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: none;
    z-index: 42;
}

.context {
    position: absolute;
    list-style: none;
    width: 200px;
    background-color: white;
    box-shadow: rgba(0, 0, 0, 0.05) 0px 6px 24px 0px, rgba(0, 0, 0, 0.08) 0px 0px 0px 1px;
    font-weight: 400;
    border-radius: 0.7rem;
    text-align: left;
    line-height: 1.8rem;
    padding: 1rem;
    z-index: 100;
    top: 50%;
    left: 50%;
    transform: translateX(-100%) translateX(-15px) translateY(-50%);
}

.context li {
    cursor: pointer;
}

.context li:hover {
    background-color: gray;
}
</style>