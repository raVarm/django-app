$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.p_cart').click(function(){
    var id = $(this).attr('pid').toString();
    var span = this.parentNode.children[2];

    $.ajax({
        type: 'GET',
        url: '/quantitycart',
        data: {
            product_id : id,
            opr : "p"
        },
        success: function(data){
            // document.getElementsByClassName('cartQuantity').innerText = data.quantity
            span.innerText = data.quantity
            document.getElementById('amount').innerText = data.amount
            document.getElementById('totalamount').innerText = data.totalamount
        }
    })
})

$('.m_cart').click(function(){
    var id = $(this).attr('pid').toString();
    var span = this.parentNode.children[2];

    $.ajax({
        type: 'GET',
        url: '/quantitycart',
        data: {
            product_id : id,
            opr : "m"
        },
        success: function(data){
            // document.getElementsByClassName('cartQuantity').innerText = data.quantity
            span.innerText = data.quantity
            document.getElementById('amount').innerText = data.amount
            document.getElementById('totalamount').innerText = data.totalamount

        }
    })
})

$('.remove_cart').click(function(){
    var id = $(this).attr('pid').toString();
    var remove_btn = this

    $.ajax({
        type: 'GET',
        url: '/quantitycart',
        data: {
            product_id : id,
            opr : "r"
        },
        success: function(data){
            document.getElementById('amount').innerText = data.amount
            document.getElementById('totalamount').innerText = data.totalamount
            remove_btn.parentNode.parentNode.parentNode.parentNode.remove()
        }
    })
})