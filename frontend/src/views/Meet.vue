<template>
  <div class="row justify-content-center">
    <div class="col-lg-5 col-md-7">
      <div class="card bg-secondary shadow border-0">
        <div class="card-body px-lg-5 py-lg-5">
          <div class="text-center text-muted mb-4">
            <small>Meeting Url</small>
          </div>
          <form role="form" @submit.prevent="">
            <base-input
              alternative
              type="text"
              v-model="meetingUrl"
              placeholder="https://olden.ai/meet/abcd"
              @blur="$v.meetingUrl.$touch()"
              addon-left-icon="ni ni-email-83"
              :error="invalidUrl"
            >
            </base-input>

            <div class="text-center">
              <base-button
                :disabled="!isValidForm"
                type="primary"
                @click="submitForm"
                class="my-4"
                >Go to Meeting</base-button
              >
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { url, required } from "vuelidate/lib/validators";
import axios from "../axios-auth";

export default {
  name: "attend",
  data: () => ({
    meetingUrl: null,
  }),
  validations: {
    meetingUrl: {
      required,
      url,
    },
  },
  computed: {
    isValidForm() {
      return !this.$v.meetingUrl.$invalid;
    },
    invalidUrl() {
      if (this.$v.meetingUrl.$error) {
        return "Please enter a valid meeting URL.";
      }
      return "";
    },
  },
  methods: {
    clearForm() {
      this.meetingUrl = null;
    },
    async submitForm() {
      if (this.isValidForm) {
        await axios
          .get("meet/redirect", {
            params: { meetingUrl: this.meetingUrl },
          })
          .then((res) => {
            this.$message.success("You are being redirected to the meeting");
            window.location.href = res.meeting_url;
          })
          .catch((error) => {
            this.$message.error(error.response.data.message);
            this.clearForm();
            this.$v.$reset();
          });
      }
    },
  },
  mounted() {},
};
</script>
<style></style>
