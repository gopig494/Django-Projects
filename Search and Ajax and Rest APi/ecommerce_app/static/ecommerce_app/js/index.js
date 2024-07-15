async function add_to_cart(eve,product_id,product_name,url,price,old_price,auth){
   
    console.log("--event-->",eve.target.id)

    if(auth){

       

        // $.ajaxSetup({
        //     beforeSend: function(xhr, settings) {
        //         xhr.setRequestHeader("X-CSRFToken", csrftoken);
        //     }
        // });
    
        data = {
            'product_id':product_id,
            'product_name': product_name,
            'url': url,
            'price': price,
            'old_price': old_price,
            // 'cart_qty': cart_qty,
            // 'cart_id': cart_id
        }
    
        let resp = await api_call_3(data,'/ecommerce/add-to-cart/');
        if (resp && resp.status == "success"){
            // alert(`The Product ${product_name} added successfully.` )
            window.location.reload();
        }
        else{
            alert('Something went wrong.Try again latter.')
        }        
    }
    else{
        alert("Please login or signup to add product to cart.")
    }
}

async function update_cart(qty,cart_id,auth){
    if(auth){
        let data = {
            "cart_id":cart_id
        }

        // localStorage.setItem("cart_id",cart_id)
        // localStorage.removeItem("cart_id")

        let resp = await api_call_3(data,'/ecommerce/add-to-cart/')
        if (resp && resp.status == "success"){
            // alert(`The Product ${product_name} added successfully.` )
            window.location.reload();
        }
        else{
            alert('Something went wrong.Try again latter.')
        }      
    }
    else{
        alert("You are not authrozed user.")
    }
}

async function delete_cart(qty,cart_id,auth){
    if(auth){
        let data = {
            "cart_id":cart_id
        }

        // localStorage.setItem("cart_id",cart_id)
        // localStorage.removeItem("cart_id")

        let resp = await api_call_3(data,'/ecommerce/delete-cart/')
        if (resp && resp.status == "success"){
            // alert(`The Product ${product_name} added successfully.` )
            window.location.reload();
        }
        else{
            alert('Something went wrong.Try again latter.')
        }      
    }
    else{
        alert("You are not authrozed user.")
    }
}


function api_call_3(data,url){
    return new Promise((resolve,reject) =>{
        csrftoken = getCookie('csrftoken')
        $.ajax({
            type: 'POST',
            url: url, // URL of your Django view
            async:false,
            headers:{
                'X-CSRFToken': csrftoken
            },
            // dataType: 'json',
            data: data,
            success: function(data, textStatus, xhr) {
                console.log('--xhr-->',xhr.status);
                console.log('--data-->',data);
                console.log('--textStatus-->',textStatus);

                resolve(data) 
            },
            error: function(xhr, status, error) {
                console.log('--xhr-->',xhr.status);
                console.log('--status-->',status);
                console.log('--error-->',error);
                resolve({"status":'failed',error:error})
            },
            // complete: function(xhr, status) {
            //     console.log('Request complete',status);
            //     console.log('Request complete --xhr-->',xhr);
            //   }
        });
    })
}


async function api_call_2(data,url){
    try {
        const csrftoken = getCookie('csrftoken');
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const responseData = await response.json();
        return responseData;
    } catch (error) {
        console.error('Fetch error:', error);
        return { status: 'failed', error: error.message };
    }
}


async function api_call(data,url){
    csrftoken = getCookie('csrftoken')
    await $.ajax({
        type: 'POST',
        url: url, // URL of your Django view
        async:false,
        headers:{
            'X-CSRFToken': csrftoken
        },
        // dataType: 'json',
        data: data,
        success: function(data) {
            return data
        },
        error: function(xhr, status, error) {
            console.log('--xhr-->',xhr);
            console.log('--status-->',status);
            console.log('--error-->',error);
            return {"status":'failed',error:error}
        },
        // complete: function(xhr, status) {
        //     console.log('Request complete',status);
        //     console.log('Request complete --xhr-->',xhr);
        //   }
    });

}

function getCookie(name) {
   
    let cookie_arr = document.cookie.split(";")
    let csrftoken = undefined


    for(let i = 0;i < cookie_arr.length; i++){
        if(cookie_arr[i].trim().includes("csrftoken")){
            csrftoken = decodeURIComponent(cookie_arr[i].split("=")[1])
            break
        }
    }

    console.log("--csrd-->",csrftoken)

    return csrftoken

}


