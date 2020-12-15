<template>
  <div class="row justify-content-center">
    <div class="col-lg-5 col-md-7">
      <div class="card bg-secondary shadow border-0">
        <div class="card-body px-lg-5 py-lg-5">
          <div class="text-center text-muted mb-4">
            <small>Sign up with credentials</small>
          </div>
          <form role="form">
            <base-input
              v-model="email"
              @blur="$v.email.$touch()"
              alternative
              class="mb-3"
              placeholder="Email"
              addon-left-icon="ni ni-email-83"
              name="email"
              :error="invalidEmail"
            >
            </base-input>

            <base-input
              v-model="password"
              alternative
              class="mb-3"
              @blur="$v.password.$touch()"
              type="password"
              name="password"
              placeholder="Password"
              addon-left-icon="ni ni-lock-circle-open"
              :error="invalidPassword"
            >
            </base-input>

            <base-input
              v-model="passwordConfirmation"
              alternative
              @blur="$v.passwordConfirmation.$touch()"
              class="mb-3"
              type="password"
              name="passwordConfirmation"
              placeholder="Confirm Password"
              addon-left-icon="ni ni-lock-circle-open"
              :error="invalidPasswordConfirmation"
            >
            </base-input>

            <base-input
              v-if="constants.needInvitationCode"
              v-model="invitationCode"
              alternative
              class="mb-3"
              type="text"
              name="invitationCode"
              @blur="$v.invitationCode.$touch()"
              placeholder="Invitation Code"
              addon-left-icon="fa fa-user-secret"
              :error="invalidInvitationCode"
            >
            </base-input>

            <div class="text-center">
              <base-button
                :disabled="!isValidForm"
                type="primary"
                class="my-4"
                @click="submitForm"
                >Create account</base-button
              >
            </div>
          </form>
        </div>
      </div>
      <div class="row mt-3">
        <div class="col-6">
          <a href="#" class="text-primary">
            <small>Forgot password?</small>
          </a>
        </div>
        <div class="col-6 text-right">
          <router-link to="/login" class="text-primary">
            <small>Login into your account</small>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { email, required, minLength, sameAs } from "vuelidate/lib/validators";
import { Constants } from "../globals.js";
import axios from "../axios-auth";

export default {
  name: "register",
  constants: {
    constants: Constants,
  },
  data: () => ({
    email: null,
    password: null,
    passwordConfirmation: null,
    invitationCode: null,
  }),
  validations: {
    email: {
      required,
      email,
    },
    password: {
      required,
      minLength: minLength(8),
    },
    passwordConfirmation: {
      sameAs: sameAs("password"),
    },
    invitationCode: {
      required,
    },
  },
  computed: {
    isValidForm() {
      return (
        !this.$v.email.$invalid &&
        !this.$v.password.$invalid &&
        !this.$v.passwordConfirmation.invalid &&
        !(this.$v.invitationCode.$invalid && this.constants.needInvitationCode)
      );
    },
    invalidEmail() {
      if (this.$v.email.$error) {
        return "Please enter a valid email.";
      }
      return "";
    },
    invalidPassword() {
      if (this.$v.password.$error) {
        return "Password must contain at least 8 characters.";
      }
      return "";
    },
    invalidPasswordConfirmation() {
      if (this.$v.passwordConfirmation.$error) {
        return "Passwords do not match.";
      }
      return "";
    },
    invalidInvitationCode() {
      if (this.$v.invitationCode.$error && this.constants.needInvitationCode) {
        return "Must provide invitation code.";
      }
      return "";
    },
  },
  methods: {
    clearForm() {
      this.email = null;
      this.password = null;
      this.passwordConfirmation = null;
      this.invitationCode = null;
    },
    async submitForm() {
      if (this.isValidForm) {
        axios
          .post("auth/register", {
            email: this.email,
            password: this.password,
            invitationCode: this.invitationCode,
            returnSecureToken: true,
          })
          .then((res) => {
            this.$store.dispatch("signup", res.data);
          })
          .catch((error) => {
            this.$message.error(error.response.data.message);
            this.clearForm();
            this.$v.$reset();
          });
      }
    },
  },
};
</script>
<style></style>
