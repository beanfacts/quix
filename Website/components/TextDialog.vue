<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="290">
      <template v-slot:activator="{ on, attrs }">
        <v-btn color="primary" dark v-bind="attrs" v-on="on">
          <v-icon>mdi-grease-pencil</v-icon>
        </v-btn>
      </template>
      <v-card>
        <v-card-title class="headline">
          {{ this.field }}
        </v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-text-field
            label="New Configuration"
            v-model="usrInput"
          ></v-text-field>
          <v-btn color="green darken-1" text @click="updateConfig">
            Done
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import axios from 'axios'

export default {
  name: 'TextDialog',
  props: ['field', 'jsKey'],
  data() {
    return {
      dialog: false,
      usrInput: null,
      url: 'https://api.quix.click/api/v1/client/backends/modify?id=',
      Authorization: this.$auth.$storage.getState('_token.local'),
    }
  },
  methods: {
    async updateConfig() {
      this.dialog = false
      const config = {
        headers: {
          'Content-Type': 'application/json-patch+json',
          Authorization: this.Authorization, //Change this
        },
      }
      var info = {
        cmd: [
          {
            op: 'modify_kv',
            data: {},
          },
        ],
      }
      info.cmd[0].data[this.jsKey] = this.usrInput
      console.log(info)

      if (this.usrInput != null) {
        try {
          let res = await axios.patch(
            this.url + this.$route.params.id,
            JSON.stringify(info),
            config
          )
          console.log("Text Dialog:",res)
        } catch (error) {
          console.log(error)
        }
        this.$emit('item-changed', this.jsKey, this.usrInput)
      }
    },
  },
}
</script>

<style>
</style>