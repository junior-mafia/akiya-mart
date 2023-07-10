interface TaskData {
  message: string
}

const executeRundateTask = async (): Promise<TaskData> => {
  const response = await fetch("/admin/rundate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
  const data = await response.json()
  if (!response.ok) {
    const message = `${data.message}`
    throw new Error(message)
  } else {
    return data.results
  }
}

const executeListingsAthomeTask = async (): Promise<TaskData> => {
  const response = await fetch("/admin/listings-athome", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
  const data = await response.json()
  if (!response.ok) {
    const message = `${data.message}`
    throw new Error(message)
  } else {
    return data.results
  }
}

const executeListingsNiftyTask = async (): Promise<TaskData> => {
  const response = await fetch("/admin/listings-nifty", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
  const data = await response.json()
  if (!response.ok) {
    const message = `${data.message}`
    throw new Error(message)
  } else {
    return data.results
  }
}

const executeListingsDetailsAthomeTask = async (): Promise<TaskData> => {
  const response = await fetch("/admin/listings-details-athome", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
  const data = await response.json()
  if (!response.ok) {
    const message = `${data.message}`
    throw new Error(message)
  } else {
    return data.results
  }
}

const executeListingsDetailsNiftyTask = async (): Promise<TaskData> => {
  const response = await fetch("/admin/listings-details-nifty", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
  const data = await response.json()
  if (!response.ok) {
    const message = `${data.message}`
    throw new Error(message)
  } else {
    return data.results
  }
}
 
export { 
  executeRundateTask, 
  TaskData, 
  executeListingsAthomeTask, 
  executeListingsNiftyTask, 
  executeListingsDetailsAthomeTask,
  executeListingsDetailsNiftyTask
}
