<script setup>
import { nextTick, ref } from 'vue'

const props = defineProps(['value'])
const emit = defineEmits(['edit'])

const isBeingEdited = ref(false)

const entryInput = ref(null)

async function onEdit() {
    isBeingEdited.value = true

    await nextTick()

    if (entryInput.value) {
        entryInput.value.select()
        entryInput.value.focus()
    }
}

function onEditInputKeyUp(event) {
    if (event.key === "Enter") {
        isBeingEdited.value = false
        emit('edit', event.target.value)
    }
}

function onStopEditing() {
    isBeingEdited.value = false
}

</script>


<template>
    <div class="editable-table-entry">
        <input ref="entryInput" v-if="isBeingEdited" type="text" :value="value" @keyup="onEditInputKeyUp">
        <div v-if="isBeingEdited" class="click-intercept" @click.stop="onStopEditing"></div>
        <span @click.stop="onEdit">{{ value }}</span>
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
.editable-table-entry {
    position: relative;
    display: inline-block;
}

.editable-table-entry span:hover {
    color: blue;
    cursor: text;
}

.editable-table-entry input {
    position: absolute;
    border-style: none;
    outline: none;
    height: 1.5rem;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
}
</style>