function confirmAction(event) {
    var result = confirm("Вы уверены, что хотите удалить аккаунт ?");

    if (result) {
        /*
        document.getElementById("form_for_delete_user_account").submit();
         */
    } else {
        event.preventDefault();
    }

}