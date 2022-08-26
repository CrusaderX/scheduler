import { defineStore } from "pinia";

export const useBoardsStore = defineStore({
  id: "board",
  state: () => ({
    board: {},
    selectedColumn: 0,
    selectedTask: 0,
  }),
  getters: {
    getColumns: (state) => state.board?.columns,
    getCurrentBoard: (state) => state.board,
    getCurrentColumn: (state) =>
      state.board?.columns[state.selectedColumn],
    getTask: (state) =>
      state.board?.columns[state.selectedColumn].tasks[state.selectedTask],
    getColumnsNames: (state) =>
      state.board?.columns.map((c) => c.name),
  },
  actions: {
    changeTaskColumn(index) {
      if (!(index === this.selectedColumn)) {
        this.getCurrentBoard?.columns[index]?.tasks.push(this.getTask);
        this.getCurrentColumn?.tasks.splice(this.selectedTask, 1);
        this.selectedColumn = index;
        this.selectedTask = this.getCurrentColumn?.tasks.length - 1;
      }
    },
    saveTaskChanges({ task, column }) {
      this.getCurrentColumn.tasks[this.selectedTask] = task;
      if (this.selectedColumn !== column) {
        this.changeTaskColumn(column);
      }
    },
  },
});
