<script setup>
import router from '../router'
import { ref, onMounted } from 'vue'

import { store } from '../store/store'
import { api } from '../store/api'

import DataTableContainer from '../components/DataTableContainer.vue'
import EditableTableEntry from '../components/EditableTableEntry.vue'
import RowContextMenu from '../components/RowContextMenu.vue'

const workouts = ref(null)

async function fetchWorkouts() {
    const response = await api.getWorkouts(store.accessToken)
    if (!response.ok) {
        console.log("Unable to fetch workouts!")
        return
    }
    const fetchedWorkouts = await response.json()
    workouts.value = fetchedWorkouts
}

onMounted(fetchWorkouts)

async function addWorkout() {
    const response = await api.createWorkout("MyWorkout", store.accessToken)
    if (!response.ok) {
        console.log("Unable to add workout!")
        return
    }
    const addedWorkout = await response.json()
    workouts.value.push(addedWorkout)
}

async function duplicateWorkout(workoutId) {
    const response = await api.copyWorkout(workoutId, store.accessToken)
    if (!response.ok) {
        console.log("Unable to duplicate workout!")
        return
    }
    const duplicatedWorkout = await response.json()
    workouts.value.push(duplicatedWorkout)
}

async function editWorkout(workoutId, field, value) {
    const response = await api.updateWorkout(workoutId, field, value, store.accessToken)
    if (!response.ok) {
        console.log("Unable to edit workout!")
        return
    }
    const editedWorkout = await response.json()
    workouts.value = workouts.value.map((workout) => 
                                workout.id == editedWorkout.id ? {...editedWorkout} : workout)
}

async function removeWorkout(workoutId) {
    const response = await api.deleteWorkout(workoutId, store.accessToken)
    if (!response.ok) {
        console.log("Unable to remove workout!")
        return
    }

    const removedWorkout = await response.json()
    workouts.value = workouts.value.filter((workout) => workout.id != removedWorkout.id)
}

function sortWorkoutById(workoutA, workoutB) {
    return workoutB.id - workoutA.id
}

const workoutContextMenuActions = [
    {
        name: "copy",
        text: "Copy as blueprint"
    },
    {
        name: "delete",
        text: "Delete"
    }
]

function dispatchWorkoutContextMenuAction(workoutId, actionName) {
    switch (actionName) {
        case "copy":
            duplicateWorkout(workoutId)
            break
        case "delete":
            removeWorkout(workoutId)
            break
        default:
            console.log("Unhandled action in dispatchWorkoutContextMenuAction")
    }
}

function navigateToWorkout(workoutId) {
    router.push(`/workouts/${workoutId}`)
}
</script>

<template>
    <DataTableContainer :title="'Home'" :action="'Add workout'" @create="addWorkout">
        <thead>
            <th>Name</th>
            <th>Date</th>
            <th>&nbsp;</th>
        </thead>
        <p v-if="!workouts">Loading workouts...</p>
        <tbody v-else>
            <tr v-for="workout in workouts.sort(sortWorkoutById)" @click.stop="() => navigateToWorkout(workout.id)">
                <td>
                    <EditableTableEntry :value="workout.name" @edit="(value) => editWorkout(workout.id, 'name', value)" />
                </td>
                <td>
                    {{ workout.date.split('T')[0] }}
                </td>
                <td>
                    <RowContextMenu :actions="workoutContextMenuActions" @action-click="(actionName) => dispatchWorkoutContextMenuAction(workout.id, actionName)" />
                </td>
            </tr>
        </tbody>
    </DataTableContainer>
</template>