<template>
  <v-card>
    <v-card-title>Login</v-card-title>
    <v-card-text>
      <v-form v-model="isValid">
        <v-text-field
          label="Username"
          v-model="username"
          required
          :rules="[(v) => !!v || 'Username is required']"
        ></v-text-field>
        <v-text-field
          label="Password"
          v-model="password"
          type="password"
          required
          :rules="[(v) => !!v || 'Password is required']"
        ></v-text-field>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-btn color="#0f4c75" :disabled="!isValid" @click="loginUser"
        >Login</v-btn
      >
    </v-card-actions>
  </v-card>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      username: null,
      password: null,

      mockLogin: {
        username: 'matty',
        password: 'matty01',
      },
      isValid: null,
      url: 'https://api.quix.click/api/v1/client/auth',
    }
  },
  methods: {
    async loginUser() {
      try {
        let res = await this.$auth.loginWith('local', {
          data: { username: this.username, password: this.password },
        })
        this.$router.push('/servers')
        this.$forceUpdate()
        // console.log('Login Page:', res)
        this.updateToken(res.data.token)

      } catch (error) {
        console.log(error)
      }
    },
    async updateToken(data) {
      this.$store.commit("setToken",data)
    },
  },
}
</script>

<style>
</style>