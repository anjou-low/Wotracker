const BASE_API_URL = import.meta.env.VITE_BASE_API_URL

export const api = {
    url: BASE_API_URL,

    async register(username, password) {
        return api.post(`${api.url}/users`, {username: username, password: password})
    },
    async authenticate(username, password) {
        const response = await fetch(`${api.url}/token`, {
            method: "POST",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({
                'username': username,
                'password': password
            })
        })

        return response
    },

    async post(url, body, token) {
        const request = new Request(url, {
            method: "POST",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        })
        
        if (token) {
            request.headers.append("Authorization", `Bearer ${token}`)
        }

        const response = await fetch(request)
        return response
    },

    async get(url, token) {
        const request = new Request(url, {
            method: "GET",
            headers: {
                "Accept": "application/json"
            }
        })

        if (token) {
            request.headers.append("Authorization", `Bearer ${token}`)
        }

        const response = await fetch((request))
        return response
    },

    async patch(url, body, token) {
        const request = new Request(url, {
            method: "PATCH",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        })

        if (token) {
            request.headers.append("Authorization", `Bearer ${token}`)
        }

        const response = await fetch(request)
        return response
    },

    async delete(url, token) {
        const request = new Request(url, {
            method: "DELETE",
            headers: {
                "Accept": "application/json"
            }
        })

        if (token) {
            request.headers.append("Authorization", `Bearer ${token}`)
        }

        const response = await fetch(request)
        return response
    },

    async getWorkouts(token) {
        return api.get(`${api.url}/workouts`, token)
    },
    async getWorkout(workoutId, token) {
        return api.get(`${api.url}/workouts/${workoutId}`, token)
    },
    async createWorkout(name, token) {
        return api.post(`${api.url}/workouts`, {name: name}, token)
    },
    async copyWorkout(workoutId, token) {
        return api.post(`${api.url}/workouts/${workoutId}/copy`, null, token)
    },
    async updateWorkout(workoutId, field, value, token) {
        return api.patch(`${api.url}/workouts/${workoutId}`, {[field]: value}, token)
    },
    async deleteWorkout(workoutId, token) {
        return api.delete(`${api.url}/workouts/${workoutId}`, token)
    },
    async getExercises(workoutId, token) {
        return api.get(`${api.url}/workouts/${workoutId}/exercises`, token)
    },
    async getExercise(workoutId, exerciseId, token) {
        return api.get(`${api.url}/workouts/${workoutId}/exercises/${exerciseId}`, token)
    },
    async createExercise(workoutId, name, token) {
        return api.post(`${api.url}/workouts/${workoutId}/exercises`, {name: name, tags: []}, token)
    },
    async updateExercise(workoutId, exerciseId, field, value, token) {
        return api.patch(`${api.url}/workouts/${workoutId}/exercices/${exerciseId}`, {[field]: value}, token)
    },
    async deleteExercise(workoutId, exerciseId, token) {
        return api.delete(`${api.url}/workouts/${workoutId}/exercises/${exerciseId}`, token)
    },
    async getSets(workoutId, exerciseId, token) {
        return api.get(`${api.url}/workouts/${workoutId}/exercises/${exerciseId}/sets`, token)
    },
    async getSet(workoutId, exerciseId, setId, token) {
        return api.get(`${api.url}/workouts/${workoutId}/exercises/${exerciseId}/sets/${setId}`, token)
    },
    async createSet(workoutId, exerciseId, weight, repetitions, token) {
        return api.post(`${api.url}/workouts/${workoutId}/exercises/${exerciseId}/sets/`, {weight: weight, repetitions: repetitions}, token)
    },
    async updateSet(workoutId, exerciseId, setId, field, value, token) {
        return api.patch(`${api.url}/workouts/${workoutId}/exercises/${exerciseId}/sets/${setId}`, {[field]: value}, token)
    },
    async deleteSet(workoutId, exerciseId, setId, token) {
        return api.delete(`${api.url}/workouts/${workoutId}/exercises/${exerciseId}/sets/${setId}`, token)
    }
}