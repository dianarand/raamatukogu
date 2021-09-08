export function showForLender() {
  if (localStorage.getItem('role') === 'lender') {
    return true
  } else {
    return false
  }
}

export function showForBorrower() {
  if (localStorage.getItem('role') === 'borrower') {
    return true
  } else {
    return false
  }
}

export function alertClass(status) {
  if ([200, 201].includes(status)) {
    return "alert alert-success"
  }
   else if (status === 401) {
    return "alert alert-danger"
  } else if ([400, 404].includes(status)) {
    return "alert alert-warning"
  } else {
     return "alert alert-primary"
  }
}