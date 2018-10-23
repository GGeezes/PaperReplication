// convert JSON to CSV: https://konklone.io/json/

var fs = require('fs');

function getSample(dataset, sampleSize){
    var domain = [0, dataset.length - 1];
    var sample = [];
    var checkedNumbers = [];

    while(sample.length < sampleSize){
        var randomNumber = Math.floor(Math.random() * domain[1]);
        if(!checkedNumbers.includes(randomNumber)){
            sample.push(dataset[randomNumber])
        }
    }

    return sample;
}

let files = ["Dropbox_AppStore_reviews",
    "Evernote_AppStore_reviews",
    "TripAdvisor_AppStore_reviews",
    "PicsArt_PlayStore_reviews",
    "WhatsApp_PlayStore_reviews",
    "Pinterest_PlayStore_reviews"
];

var wholeData = [];

files.forEach(fileTitle => {
    data = JSON.parse(fs.readFileSync("reviews/"+ fileTitle +".json"));
    sampled_data = getSample(data, 100);
    sampled_data.forEach(review => {
            wholeData.push(review);
    });
});

for (let i = 0; i < 10; i++) {
    const review = wholeData[i];
    console.log(review.comment);
}

console.log(wholeData.length);

fs.writeFileSync("full_dataset.json", JSON.stringify(wholeData));