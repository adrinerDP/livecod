$.ajax({
    url: '/data/version_info.json',
    method: 'get',
    success: (data) => {
        const UPDATE_DATE = $('span#UPDATE_DATE');
        const UPDATE_TIME = $('span#UPDATE_TIME');
        const UPDATE_HASH = $('span#UPDATE_HASH');

        UPDATE_DATE.html(data.crawl_date);
        UPDATE_TIME.html(data.crawl_time_only_hour);
        UPDATE_HASH.html(data.version_hash);
    }
})