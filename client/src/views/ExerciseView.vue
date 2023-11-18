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
import EntryValueDiff from '../components/EntryValueDiff.vue'

const workout = ref(null)
const exercise = ref(null)
const sets = ref(null)
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

async function fetchExercise() {
  const response = await api.getExercise(route.params.workoutId, route.params.exerciseId, store.accessToken)
  if (!response.ok) {
    console.log("Unable to fetch exercise!")
    return
  }

  const fetchedExercise = await response.json()
  exercise.value = fetchedExercise
}

onMounted(fetchExercise)

async function fetchSets() {
    const response = await api.getSets(route.params.workoutId, route.params.exerciseId, store.accessToken)
    if (!response.ok) {
        console.log("Unable to fetch sets!")
        retur
    }

    const fetchedSets = await response.json()
    sets.value = fetchedSets
}

onMounted(fetchSets)

async function addSet() {
    const response = await api.createSet(route.params.workoutId, route.params.exerciseId, 0, 0, store.accessToken)
    if (!response.ok) {
        console.log("Unable to add set!")
        return
    }

    const addedSet = await response.json()
    sets.value.push(addedSet)
}

async function editSet(setId, fied, value) {
    const response = await api.updateSet(route.params.workoutId, route.params.exerciseId, setId, fied, value, store.accessToken)
    if (!response.ok) {
        console.log("Unable to edit set!")
        return
    }

    const editedSet = await response.json()
    sets.value = sets.value.map((set) =>
                        set.id == editedSet.id ? {...editedSet} : set)
}

async function removeSet(setId) {
    const response = await api.deleteSet(route.params.workoutId, route.params.exerciseId, setId, store.accessToken)
    if (!response.ok) {
        console.log("Unable to remove set!")
        return
    }

    const removedSet = await response.json()
    sets.value = sets.value.filter((set) => set.id != removedSet.id)
}

const setContextMenuActions = [
    {
        name: "delete",
        text: "Delete"
    }
]

function dispatchSetContextMenuAction(setId, actionName) {
    switch (actionName) {
        case "delete":
            removeSet(setId)
            break
        default:
            console.log("Unhandled action in dispatchSetContextMenuAction")
    }
}
</script>

<template>
    <Navigation :link="`/workouts/${$route.params.workoutId}`" :msg="`Back to ${workout ? workout.name : 'workout'}`" />
    <DataTableContainer :title="exercise ? exercise.name : 'Exercise'" :action="'Add set'" @create="addSet">
    <thead>
      <th>Weight</th>
      <th>Repetitions</th>
      <th>&nbsp;</th>
    </thead>
    <p v-if="!sets">Loading sets...</p>
    <tbody v-else>
      <tr v-for="set in sets">
        <td>
          <EditableTableEntry :value="set.weight" @edit="(value) => editSet(set.id, 'weight', value)"/>
          <EntryValueDiff :diffValue="set.weight_diff" />
        </td>
        <td>
          <EditableTableEntry :value="set.repetitions" @edit="(value) => editSet(set.id, 'repetitions', value)"/>
          <EntryValueDiff :diffValue="set.repetitions_diff" />
        </td>
        <td>
          <RowContextMenu :actions="setContextMenuActions" @action-click="(actionName) => dispatchSetContextMenuAction(set.id, actionName)" />
        </td>
      </tr>
    </tbody>
  </DataTableContainer>
</template>