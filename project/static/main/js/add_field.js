let inputForm = document.querySelectorAll(".media-input-form")
let container = document.querySelector("#form-container")
let addField = document.querySelector("#add-media-form")
let totalForms = document.querySelector("#id_form-TOTAL_FORMS")

let formNum = inputForm.length-1
let x = 0
addField.addEventListener('click', addForm)

function addForm(event){
    if (x < 3) {
        event.preventDefault()

        let newForm = inputForm[0].cloneNode(true)
        let formRegex = RegExp(`form-(\\d){1}-`,'g')

        formNum++
        x++
        newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`)
        container.insertBefore(newForm, addField)

        totalForms.setAttribute('value', `${formNum+1}`)
    }
}
