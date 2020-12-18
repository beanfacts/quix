// import createPersistedState from 'vuex-persistedstate'

export const state = () => ({
    token: null,
})

export const mutations = {
    setToken(state, value) {
        state.token = value
    },
}

// export const plugins = [
//     createPersistedState()
//   ]