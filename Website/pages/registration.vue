<template>
  <v-card>
    <v-card-title>Register for Quix</v-card-title>
    <v-card-text>
      <v-form v-model="isValid">
        <v-text-field
          label="Email"
          v-model="email"
          required
          :rules="emailRules"
        ></v-text-field>
        <v-text-field
          label="Password"
          v-model="password"
          type="password"
          required
          :rules="passwordRules"
        ></v-text-field>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-btn color="#0f4c75" :disabled="!isValid" @click="debug">Register</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: '',
      isValid: null,
      emailRules: [
        (v) => !!v || 'Email is required',
        (v) => /.+@.+/.test(v) || 'E-mail must be valid',
      ],
      passwordRules: [
        (v) => !!v || 'Password is required',
        (v) => (v && v.length >= 5) || 'Password must have 5+ characters',
      ],
    }
  },
  methods:{
      debug(){
          console.log("Email:"+this.email);
          console.log("Password:"+this.password)
      }
  }
}
</script>

<style>
</style>