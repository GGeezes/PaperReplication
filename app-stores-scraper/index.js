var appstore = require('app-store-scraper');
var playstore = require('google-play-scraper');
var fs = require('fs')

function saveJsonDict(appName, source, dict){
    fs.writeFileSync("reviews/" + appName + "_" + source +  "_reviews.json", JSON.stringify(dict));
}

// ## Structure of the output
// - id
// - title
// - comment
// - rating
// - reviewer
// - fee
// - date
// - dataSource (app store or play store)
// - contains (user experience, bug report, new feature request, rating)

// App Store App Reviews
function scrapeAppStoreAppReviews(apple_store_apps, num_pages_to_retrieve){

    for (let i = 0; i < apple_store_apps.length; i++) {
        
        const app = apple_store_apps[i];
        var promises = [];
        console.log(app);

        // All the promises for a single app
        for (let page = 0; page < num_pages_to_retrieve + 1; page++) {
            console.log("page: " + page);
            promises.push(appstore.reviews({
                id: app[1],
                sort: appstore.sort.RECENT,
                page: page
            }));      
        }
        console.log(promises);

        // Deal with all the promises results
        Promise.all(promises).then(results => {
            var app_store_scrapped_reviews = [];
            var app_store_reviews = [];

            results.forEach(batch => {
                batch.forEach(review => {
                    app_store_scrapped_reviews.push(review);    
                });            
            });

            app_store_reviews = app_store_scrapped_reviews.map(review => {
                return {
                    "app": app[0],
                    "id": review.id,
                    "title": review.title,
                    "comment": review.text,
                    "rating": review.score,
                    "reviewer": review.userName,
                    "fee": app[2],
                    "date": "NA",
                    "version": "114.2",
                    "data source": "npm app-store-scraper" 
                }
            });

            console.log("Length:" + app_store_reviews.length);
            saveJsonDict(app[0], "AppStore", app_store_reviews);
        })
        .catch(d => {
            console.log(d);
        });
    }
}

// Google Play Store App Reviews
function scrapePlayStoreAppReviews(play_store_apps, num_pages_to_retrieve){

    for (let i = 0; i < play_store_apps.length; i++) {
        
        const app = play_store_apps[i];
        var promises = [];
        console.log(app);

        // All the promises for a single app
        for (let page = 0; page < num_pages_to_retrieve + 1; page++) {
            console.log("page: " + page);
            promises.push(playstore.reviews({
                appId: app[1],
                page: page,
                sort: playstore.sort.NEWEST
            }));      
        }
        console.log(promises);

        // Deal with all the promises results
        Promise.all(promises).then(results => {
            var play_store_scrapped_reviews = [];
            var play_store_reviews = [];

            results.forEach(batch => {
                batch.forEach(review => {
                    play_store_scrapped_reviews.push(review);    
                });            
            });

            play_store_reviews = play_store_scrapped_reviews.map(review => {
                return {
                    "app": app[0],
                    "id": review.id,
                    "title": review.title,
                    "comment": review.text,
                    "rating": review.score,
                    "reviewer": review.userName,
                    "fee": app[2],
                    "date": review.date,
                    "version": "NA",
                    "data source": "npm google-play-store-scraper" 
                }
            });

            console.log("Length:" + play_store_reviews.length);
            saveJsonDict(app[0], "PlayStore", play_store_reviews);
        })
        .catch(d => {
            console.log(d);
        });
    }
}


appstore.reviews({
  id: '284876795',
  sort: appstore.sort.RECENT,
  page: 1
})
.then(d => console.log(d.length))
.catch(console.log);

playstore.reviews({
    appId: 'com.mojang.minecraftpe',
    page: 110,
    sort: playstore.sort.NEWEST
});
//.then(console.log, console.log)
//.catch(console.log);


// RUN FUNCTIONS TO SCRAPE
let apple_store_apps = [
    ["Dropbox", "327630330", "free"], 
    ["Evernote", "281796108", "free"],
    ["TripAdvisor", "284876795", "free"]
];

//scrapeAppStoreAppReviews(apple_store_apps, 10);

let play_store_apps = [
    ["PicsArt", "com.picsart.studio", "free"],
    ["Pinterest", "com.pinterest", "free"],
    ["WhatsApp", "com.whatsapp", "free"]
];

scrapePlayStoreAppReviews(play_store_apps, 50);