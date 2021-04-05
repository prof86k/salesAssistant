let adjustPricing = function() {
    return Math.random()
};


class SalesAssistant {
    constructor() {
        this.amount = 0;
        this.otherCharges = 0;
        this.rand = adjustPricing();
    }

    salesProfit(itemName, unitPrice, numberOfItems = 1) {
        let unit_Price = Number(unitPrice)
        let percentage = (unit_Price / (unit_Price + this.amount) * this.rand);
        if (numberOfItems > 1) {
            return {
                "Product Name": itemName,
                "Current Price": Number((percentage * unit_Price) + (unit_Price + this.otherCharges)),
                "Purchace Price": unit_Price,
                "Percentage Charge": percentage * 100,
                "Profit": Number((percentage * unit_Price) + (unit_Price + this.otherCharges)) - unit_Price,
            }
        } else {
            return {
                "Product Name": itemName,
                "Current Price": Number((percentage * unit_Price) + (unit_Price + this.otherCharges + this.amount)),
                "Purchace Price": unit_Price,
                "Percentage Charge": percentage * 100,
                "Profit": Number((percentage * unit_Price) + (unit_Price + this.otherCharges + this.amount)) - unitPrice,
            }
        }
    }

}

// //initialized the class
let seller = new SalesAssistant();

function doSaveTransport() {
    var tamount = document.getElementById("tamount").value;
    var other = document.getElementById("tothers").value;
    seller.amount = tamount;
    seller.otherCharges = other;
}




let doOnChange = function() {
    let productName = document.getElementById("productName").value;
    let unit_Price = document.getElementById("priceInput").value;
    let numberOfProducts = document.getElementById("nproducts").value;
    if (numberOfProducts) {
        let currentSeller = seller.salesProfit(itemName = String(productName), unitPrice = Number(unit_Price), numberOfItems = Number(numberOfProducts));
        document.getElementById("costPrice").innerHTML = `${currentSeller["Purchace Price"].toFixed(2)}`;
        document.getElementById("sellingPrice").innerHTML = `${currentSeller["Current Price"].toFixed(2)}`;
        document.getElementById("product_name").innerHTML = `${currentSeller["Product Name"]}`;
        document.getElementById("cprice").value = `${currentSeller["Current Price"].toFixed(2)}`;
        document.getElementById("percent").innerHTML = `${currentSeller["Percentage Charge"].toFixed(2)}`;
        document.getElementById("profit").innerHTML = `${currentSeller["Profit"].toFixed(2)}`;
    }


};

function doOnSubmit() {
    let answer = confirm(document.getElementById("productName").value + " Add Records?");
    if (answer == true) {
        let productName = document.getElementById("productName").value;
        let unit_Price = document.getElementById("priceInput").value;
        let currentSeller = seller.salesProfit(itemName = productName, unitPrice = unit_Price, numberOfItems = 30);
        document.getElementById("cprice").value = `${currentSeller["Current Price"].toFixed(2)}`;
        document.getElementById("product_name").value = `${currentSeller["Product Name"]}`;
    } else {
        alert("Correct The error and come back!");
    }

}

function popupForm() {
    document.getElementById("expenseForm").style.display = "block";
}