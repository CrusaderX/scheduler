<template>
  <header class="bg-white dark:bg-dark-grey top-0 left-0 w-full flex items-center sm:pr-4">
    <div class="mx-auto max-w-sm w-11/12 flex items-center h-16 gap-2 sm:h-20">
      <div class="flex items-center gap-2 group cursor-pointer sm:hidden">
        <h1 class="text-black dark:text-white font-bold text-lg cursor-pointer">{{ boardsStore.getCurrentBoard?.name }}</h1>
      </div>
      <h1 class="text-black dark:text-white font-bold hidden text-2xl sm:block">
        {{ boardsStore.getCurrentBoard?.name }}
      </h1>
      <div v-if="boardsStore.getCurrentBoard?.name" class="flex items-center gap-4 ml-auto">
        <PrimarySmall @click="addTask" v-if="isAuthenticated" class="hidden sm:block">+ Add new task</PrimarySmall>
        <Dropdown :isAuthenticated="isAuthenticated" target="Board" 
            @onClickEdit="editTask" @onClickDelete="deleteTask" @onClickLogin="loginUser" @onClickLogout="logoutUser"/>
      </div>
    </div>
  </header>
</template>

<script setup>

import { useBoardsStore } from '@/stores/boards';
import { useManagerStore } from '@/stores/manager';
import Dropdown from '@/components/manager/Dropdown.vue';
import IconArrowDown from './icons/IconArrowDown.vue';
import IconArrowUp from './icons/IconArrowUp.vue';
import PrimarySmall from './buttons/PrimarySmall.vue';
import { useAuth0 } from '@auth0/auth0-vue';
import { watch } from 'vue';

const { loginWithRedirect, user, isAuthenticated, logout } = useAuth0();
const boardsStore = useBoardsStore()
const managerStore = useManagerStore()
const emit = defineEmits(['onAuth'])

watch(isAuthenticated, (v, r) => {
  emit('onAuth', v);
})

const editTask = () => {
  managerStore.overlay = true
  managerStore.boardForm = { edit: true, visible: true }
}
const deleteTask = () => {
  managerStore.overlay = true
  managerStore.delete = { board: true, visible: true }
}
const addTask = () => {
  managerStore.overlay = true
  managerStore.taskForm = { visible: true, edit: false };
}

const loginUser = async () => {
  await loginWithRedirect();
  emit('onAuth', isAuthenticated);
}

const logoutUser = async () => {
  await logout({ returnTo: window.location.origin });
  emit('onAuth', isAuthenticated);
}
</script>
