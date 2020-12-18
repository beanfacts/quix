<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="290">
      <template v-slot:activator="{ on, attrs }">
        <v-btn color="#2F9E00" dark v-bind="attrs" v-on="on"
          ><v-icon>mdi-grease-pencil</v-icon></v-btn
        >
      </template>
      <v-card>
        <v-card-title class="headline"> Edit Forwarding Rule </v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-form v-model="isValid">
            <v-text-field
              :label="curProto"
              v-model="newProto"
              required
              :rules="[(v) => !!v || 'Protocol is required']"
            ></v-text-field>
            <v-text-field
              :label="String(curEport)"
              v-model="newExtPort"
              required
              :rules="[(v) => !!v || 'External Port is required']"
            ></v-text-field>
            <v-text-field
              :label="String(curIport)"
              v-model="newIntPort"
              required
              :rules="[(v) => !!v || 'Internal Port is required']"
            ></v-text-field>
          </v-form>
          <v-btn
            color="green darken-1"
            text
            @click="editRule"
            :disabled="!isValid"
          >
            Edit Rule
          </v-btn>
        </v-card-actions>
        <v-btn color="green darken-1" text @click="dialog = false">
          Cancel
        </v-btn>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import axios from 'axios'
export default {
  name: 'EditRules',
  props: ['curIP', 'curProto', 'curEport', 'curIport'],
  data() {
    return {
      newExtIP: null,
      newProto: null,
      newExtPort: null,
      newIntPort: null,
      dialog: false,
      url: 'https://api.quix.click/api/v1/client/backends/modify?id=',
      Authorization: this.$auth.$storage.getState('_token.local'),
      isValid: null,
    }
  },
  methods: {
    async editRule() {
      this.dialog = false
      const config = {
        headers: {
          'Content-Type': 'application/json',
          Authorization: this.Authorization, //Change this
        },
      }
      var info = {
        cmd: [
          {
            op: 'modify_rule',
            data: {
              from: {
                ext_ip: this.curIP,
                proto: this.curProto,
                eport: this.curEport,
                iport: this.curIport,
              },
              to: {
                ext_ip: this.curIP,
                proto: this.newProto,
                eport: parseInt(this.newExtPort),
                iport: parseInt(this.newIntPort),
              },
            },
          },
        ],
      }
      console.log('Edit Rule Component:', info.cmd[0])
      try {
        let res = await axios.patch(
          this.url + this.$route.params.id,
          info,
          config
        )
        this.$emit('update', true)
      } catch (error) {
        console.log(error)
      }
    },
  },
}
</script>

<style>
</style>