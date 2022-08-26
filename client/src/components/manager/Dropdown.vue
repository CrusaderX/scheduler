<template>
  <div tabindex="1" class="group cursor-pointer relative">
    <IconVerticalEllipsis />
    <div class="absolute right-28 top-8 hidden group-focus:block">
      <div class="bg-white dark:bg-very-dark-grey rounded-lg text-sm w-36 flex flex-col fixed z-10">
        <p @click="emit('onClickLogin')" v-if="!isAuthenticated" class="text-medium-grey text-xs font-bold w-full p-4 ">Login</p>
        <p @click="emit('onClickLogout')" v-else class="text-medium-grey text-xs font-bold w-full p-4 ">Logout</p>
        <p @click="emit('onClickEdit', target)" v-if="isAuthenticated" class="text-medium-grey text-xs font-bold w-full p-4 ">Edit {{ target }}</p>
        <p @click="emit('onClickDelete', target)" v-if="isAuthenticated" class="text-red text-xs font-bold w-full p-4 ">Delete {{ target }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import IconVerticalEllipsis from '../icons/IconVerticalEllipsis.vue';

const props = defineProps({
  isAuthenticated: {
    type: Boolean,
    required: true
  },
  target: {
    type: String,
    required: true
  }
})
const emit = defineEmits(['onClickEdit', 'onClickDelete', 'onClickLogin', 'onClickLogout'])
</script>
