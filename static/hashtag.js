
$('delete-hashtag').click(deleteHashtag)

async function deleteHashtag() {
    const id = $(this).data('id')
    await axios.delete(`/api/todos/${id}`)
    alert("DELETED!!!")
}