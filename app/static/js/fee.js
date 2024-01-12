function addToFee(id, name, fee) {
    fetch("api/fee",{
    method: "post",
    body: JSON.stringify({
        "id" : id,
        "name" : name,
        "fee" : fee
}),
headers: {
"Content-Type": "application/json"
}

    }).then(function(res){
        return res.json()
    }).then(function(data){
        console.info(data)
    })

}