<template>
  <HeaderVue @onAuth="isChanged" />
  <main>
    <div class="flex w-full ">
      <div v-dragscroll:nochilddrag
        class="relative h-full w-screen min-h-[calc(100vh-64px)] max-h-[calc(100vh-64px)] overflow-auto bg-light-grey dark:bg-very-dark-grey transition-all">
        <div data-dragscroll class="mx-auto w-11/12 pt-6 pb-24 ">
          <div data-dragscroll v-if="boardsStore.getColumns" class="flex">
            <Board data-dragscroll />
            <AddNewColumn v-if="isAuth" class="hidden md:flex"/>
          </div>
        </div>
      </div>
    </div>
  </main>
  <bgOverlay data-no-dragscroll />
  <div class="absolute top-1/2 left-1/2 translate-x-[-50%] translate-y-[-50%] z-10 max-w-xs w-11/12 sm:max-w-md">
    <TaskView v-if="managerStore.taskView" />
    <TaskForm v-if="managerStore.taskForm.visible" />
    <Delete v-if="managerStore.delete.visible" />
    <BoardForm v-if="managerStore.boardForm.visible" />
  </div>
</template >
  
<script setup>
import Board from './components/board/Board.vue'
import HeaderVue from './components/Header.vue';
import bgOverlay from './components/bgOverlay.vue';
import TaskView from './components/manager/TaskView.vue'
import TaskForm from './components/manager/TaskForm.vue';
import Delete from './components/manager/Delete.vue';
import BoardForm from './components/manager/BoardForm.vue';

import { onMounted, ref } from 'vue';
import { useBoardsStore } from '@/stores/boards.js';
import { useManagerStore } from '@/stores/manager.js';
import NoBoards from './components/board/NoBoards.vue';
import AddNewColumn from './components/board/AddNewColumn.vue';

const boardsStore = useBoardsStore();
const managerStore = useManagerStore();
const isAuth = ref(false);

onMounted(async () => {
  boardsStore.$subscribe((mutations, state) => {
    localStorage.setItem('data', JSON.stringify(state))
  })
  const storageData = localStorage.getItem("data")
  if (!storageData) {
    const jsonData = await import("./assets/json/data.json")
    boardsStore.board = jsonData.board;
  } else {
    boardsStore.$state = JSON.parse(storageData)
  }
}) 

const isChanged = (auth) => {
  isAuth.value = auth
}
</script>
