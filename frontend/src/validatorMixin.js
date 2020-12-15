export default {
  methods: {
    isValidStringWithSpaces(value) {
      return /^[a-zA-Z\s]*$/.test(value);
    },
    isPhone(value) {
      /^[0-9]{10}$/.test(value);
    },
  },
};
