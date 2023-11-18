<script setup>
import { ref, onMounted } from 'vue'
import router from '../router'
import { useRoute } from 'vue-router'

import { store } from '../store/store'
import { api } from '../store/api'

import Navigation from '../components/Navigation.vue'
import DataTableContainer from '../components/DataTableContainer.vue'
import EditableTableEntry from '../components/EditableTableEntry.vue'
import RowContextMenu from '../components/RowContextMenu.vue'

const workout   = ref(null)
const exercises = ref(null)
const route = useRoute()

async function fetchWorkout() {
    const response = await api.getWorkout(route.params.workoutId, store.accessToken)
    if (!response.ok) {
        console.log("Unable to fetch workout!")
        return
    }

    const fetchedWorkout = await response.json()
    workout.value = fetchedWorkout
}

onMounted(fetchWorkout)

async function fetchExercises() {
    const response = await api.getExercises(route.params.workoutId, store.accessToken)
    if (!response.ok) {
        console.log("Unable to fetch exercises!")
        return
    }

    const fetchedExercises = await response.json()
    exercises.value = fetchedExercises
}

onMounted(fetchExercises)

async function addExercise() {
    const response = await api.createExercise(route.params.workoutId, "MyExercise", store.accessToken)
    if (!response.ok) {
        console.log("Unable to add exercise!")
        return
    }

    const addedExercise = await response.json()
    exercises.value.push(addedExercise)
}

async function editExercise(exerciseId, field, value) {
    const response = await api.updateExercise(route.params.workoutId, exerciseId, field, value, store.accessToken)
    if (!response.ok) {
        console.log("Unable to edit exercise!")
        return
    }

    const editedExercise = await response.json()
    exercises.value = exercises.value.map((exercise) =>
                                    exercise.id == editedExercise.id ? {...editedExercise} : exercise)
}

async function removeExercise(exerciseId) {
    const response = await api.deleteExercise(route.params.workoutId, exerciseId, store.accessToken)
    if (!response.ok) {
        console.log("Unable to remove exercise!")
        return
    }

    const removedExercise = await response.json()
    exercises.value = exercises.value.filter((exercise) => exercise.id != removedExercise.id)
}

const exerciseContextMenuActions = [
    {
        name: "delete",
        text: "Delete"
    }
]

function dispatchExerciseContextMenuAction(exerciseId, actionName) {
    switch (actionName) {
        case "delete":
            removeExercise(exerciseId)
            break
        default:
            console.log("Unhandled action in dispatchWorkoutContextMenuAction")
    }
}

function navigateToExercise(exerciseId) {
    router.push(`/workouts/${route.params.workoutId}/exercises/${exerciseId}`)
}

</script>

<template>
    <Navigation :link="'/'" :msg="'Back to Home'" />
    <DataTableContainer :title="workout ? workout.name : 'Workout'" :action="'Add exercise'" @create="addExercise">
        <thead>
            <th>Name</th>
            <th>&nbsp;</th>
        </thead>
        <p v-if="!exercises">Loading exercises...</p>
        <tbody v-else>
            <tr v-for="exercise in exercises" @click.stop="() => navigateToExercise(exercise.id)">
                <td>
                    <EditableTableEntry :value="exercise.name" @edit="(value) => editExercise(exercise.id, 'name', value)" />
                </td>
                <td>
                    <RowContextMenu :actions="exerciseContextMenuActions" @action-click="(actionName) => dispatchExerciseContextMenuAction(exercise.id, actionName)" />
                </td>
            </tr>
        </tbody>
    </DataTableContainer>
</template>