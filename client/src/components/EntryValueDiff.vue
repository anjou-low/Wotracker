<script setup>
import { computed } from 'vue';

const props = defineProps({
    diffValue: Number,
})

const diffString = computed(() => {

    return props.diffValue > 0
        ? `+${props.diffValue.toFixed(1)}`
        : `${props.diffValue.toFixed(1)}`
})

const diffClass = computed(() => {
    if (props.diffValue > 0) {
        return "positive-diff"
    }
    else if (props.diffValue < 0) {
        return "negative-diff"
    }
    else
    {
        return "neutral-diff"
    }
})

</script>

<template>
    <span v-if="diffValue" :class="diffClass">{{ diffString }}</span>
</template>

<style scoped>
    span {
        margin-left: 1rem;
    }
    .positive-diff {
        color: green;
    }
    .neutral-diff {
        color: yellow;
    }

    .negative-diff {
        color: red;
    }
</style>