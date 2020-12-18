<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="290">
      <template v-slot:activator="{ on, attrs }">
        <v-btn color="primary" dark v-bind="attrs" v-on="on"> Add Rule </v-btn>
      </template>
      <v-card>
        <v-card-title class="headline"> Add Forwarding Rule </v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-form>
            <!-- <v-text-field label="External IP" v-model="newExtIP"></v-text-field> -->
            <!-- <v-card-text>{{ ExtIP }}</v-card-text> -->
            <v-text-field label="Protocol" v-model="newProto"></v-text-field>
            <v-text-field
              label="External Port"
              v-model="newExtPort"
            ></v-text-field>
            <v-text-field
              label="Internal Port"
              v-model="newIntPort"
            ></v-text-field>
          </v-form>
          <v-btn color="green darken-1" text @click="addNewRule">
            Add Rule
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import axios from 'axios'
export default {
  name: 'AddRulesDialog',
  props: ['ExtIP'],
  data() {
    return {
      newExtIP: null,
      newProto: null,
      newExtPort: null,
      newIntPort: null,
      dialog: false,
      url: 'https://api.quix.click/api/v1/client/backends/modify?id=',
      Authorization: this.$auth.$storage.getState('_token.local'),
    }
  },
  methods: {
    async addNewRule() {
      this.dialog = false
      const config = {
        headers: {
          'Content-Type': 'application/json',
          Authorization: this.Authorization, //Change this
        },
      }
      console.log('Debug:', this.ExtIP[0].ext_ip)
      const test = {
        cmd: [
          {
            op: 'create_rule',
            data: {
              ext_ip: this.ExtIP[0].ext_ip,
              proto: this.newProto,
              eport: parseInt(this.newExtPort),
              iport: parseInt(this.newIntPort),
            },
          },
        ],
      }

      //console.log(info.cmd[0])
      var temp = JSON.stringify(test)
      try {
        let res = await axios.patch(
          this.url + this.$route.params.id,
          temp,
          config
        )
        this.$emit("update",true)
      } catch (error) {
        console.log(error)
      }
    },
  },
}
</script>

<style>
</style>