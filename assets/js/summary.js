details = document.querySelectorAll("details");
details.forEach((targetDetail) => {
    targetDetail.addEventListener("click", () => {
        details.forEach((detail) => {
            if (detail !== targetDetail) {
                detail.removeAttribute("open");
            }
        });
    });
});


var admonition_title = function (target, type) {
    var html = target.innerHTML;
    const title = /(title:.*)/gi;
    const title_found = html.match(title, 'g') ;
    const admonition = {
        "note": "note",
        "seealso": "note",
        "abstract": "abstract",
        "summary": "abstract",
        "tldr": "abstract",
        "info": "todo",
        "todo": "todo",
        "tip": "tip",
        "hint": "tip",
        "important": "tip",
        "success": "done",
        "check": "done",
        "done": "done",
        "question": "question",
        "help": "question",
        "faq": "question",
        "warning": "warning",
        "caution": "warning",
        "attention": "warning",
        "failure": "failure",
        "fail": "failure",
        "missing": "failure",
        "danger": "danger",
        "error": "danger",
        "bug": "bug",
        "example": "example",
        "exemple": "example",
        "quote": "quote",
        "cite": "quote",
    };
    const html_type=admonition[type];
    if (title_found) {
        const length = title_found.length;
        for (var i = 0; i < length; i++) {
            html = html.replace(title_found[i], '<span class="' + html_type + '">' + title_found[i].replace('title:', '') + '</span>')
            target.innerHTML = html;
        }}
};

var admo_noblock = function(target) {
    var html = target.innerHTML;
    let select ='';
    let query='';
    const adm= ['note', 'seealso', 'abstract', 'summary', 'tldr', 'info', 'todo', 'tip',
                'hint', 'important', 'success', 'check', 'done', 'question', 'help', 'faq', 'warning',
                'caution', 'attention', 'failure', 'fail', 'missing', 'danger', 'error', 'bug', 'example', 'exemple', "abstract",
                'quote', 'cite'];
    const p_search = /<p>[?!]{3}ad-([A-Za-zÀ-ÖØ-öø-ÿ]+)/gi;
    const found_p = html.match(p_search);
    let select_html=''
    if (found_p) {
        const p_len = found_p.length;
        for (var i = 0; i < p_len; i++) {
            select = found_p[i].replace('!!!ad-', '');
            select = select.replace('???ad-', '');
            if (adm.includes(select)) {
                query = "<p class = admo-'" + select + "'>";
                select_html = '.admo-' + select
            } else {
                query = "<p class='admo-note'>";
                select_html = '.admo-note'
            }
            html = html.replace(p_search, query);
            html = html.replace('<br>', '');
            target.innerHTML = html;
            let html_truc = document.querySelector(select_html).innerHTML
            const p_title = /title:(.*)/gi
            const adm_title = html_truc.match(p_title)
            if (adm_title) {
                for (var j = 0; j < adm_title.length; j++) {
                    html_truc = html_truc.replace(adm_title[j], "<span class='title-" +
                        select_html.replace('.', '') + "'>" + adm_title[j].replace('title:', '') +"</span><br>")
                }
            }
            document.querySelector(select_html).innerHTML = html_truc
        }

    }
}
admo_noblock(document.querySelector('.content'))

var no_admo = function (target) {
    var html = target.innerHTML;
    const regex = /language-ad-([A-Za-zÀ-ÖØ-öø-ÿ]+)/gi;
    const found = html.match(regex);
    const adm= ['note', 'seealso', 'abstract', 'summary', 'tldr', 'info', 'todo', 'tip',
'hint', 'important', 'success', 'check', 'done', 'question', 'help', 'faq', 'warning',
    'caution', 'attention', 'failure', 'fail', 'missing', 'danger', 'error', 'bug', 'example', 'exemple', "abstract",
'quote', 'cite']
    let select = '';
    let query = '';
    if (found) {
        length = found.length;
        for (var i = 0;i<length;i++) {
            select = found[i].replace('language-ad-', '')
            query = '.' + found[i]
            if (adm.includes(select)) {
                admonition_title(document.querySelector(query), select)
            }
            else {
                document.querySelector(query).className="language-ad-note";
                admonition_title(document.querySelector('.language-ad-note'), 'note')
            }
        }
    }
}

no_admo(document.querySelector('.content'))

