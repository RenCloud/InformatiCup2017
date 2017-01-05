using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Net;
using System.Threading.Tasks;
using System.Web.Mvc;
using System.Web.Security;
using GitRepoToJSON.Models;
using Newtonsoft.Json;
using Octokit;
using Author = GitRepoToJSON.Models.Author;
using Commit = GitRepoToJSON.Models.Commit;
using Issue = Octokit.Issue;
using Language = GitRepoToJSON.Models.Language;

namespace GitRepoToJSON.Controllers {
    /// <summary>
    ///     Site Controller
    /// </summary>
    /// <remarks>Handle the entirety site call's and return the website</remarks>
    public class HomeController : Controller {
        /// <summary>
        ///     oAuth Client ID
        /// </summary>
        private const string ClientId = "a97b3ff30ea37904a570";

        /// <summary>
        ///     oAuth Client Secret
        /// </summary>
        private const string ClientSecret = "aaf90eb8b87de2ca40c995f6ac55eec85f4c1170";

        /// <summary>
        ///     GitHubClient from Octokit to connect to the API
        /// </summary>
        private readonly GitHubClient client = new GitHubClient(new ProductHeaderValue("ReproAnalyser"));

        /// <summary>
        ///     Open Index page (Mainpage)
        /// </summary>
        /// <returns>Index View</returns>
        public ActionResult Index() {
            return View();
        }

        /// <summary>
        ///     This is the Callback URL that the GitHub OAuth Login page will redirect back to.
        /// </summary>
        /// <remarks>Handle the oAuth token that is given from API when Login Correct</remarks>
        /// <param name="code">Code</param>
        /// <param name="state">State</param>
        /// <returns>Index Page </returns>
        public async Task<ActionResult> Authorize(string code, string state) {
            if (string.IsNullOrEmpty(code)) {
                return RedirectToAction("Index");
            }
            var expectedState = Session["CSRF:State"] as string;
            if (state != expectedState) {
                throw new InvalidOperationException("SECURITY FAIL!");
            }
            Session["CSRF:State"] = null;

            var token = await client.Oauth.CreateAccessToken(new OauthTokenRequest(ClientId, ClientSecret, code));
            Session["OAuthToken"] = token.AccessToken;

            return RedirectToAction("Index");
        }

        /// <summary>
        ///     Get the Url from Login Page from Github oAuth
        /// </summary>
        /// <returns>Url Login Page</returns>
        private string GetOauthLoginUrl() {
            var csrf = Membership.GeneratePassword(24, 1);
            Session["CSRF:State"] = csrf;

            // 1. Redirect users to request GitHub access
            var request = new OauthLoginRequest(ClientId) {
                Scopes = {"user", "notifications", "repo", "repo:status", "public_repo"},
                State = csrf
            };
            var oauthLoginUrl = client.Oauth.GetGitHubLoginUrl(request);
            return oauthLoginUrl.ToString();
        }
        

        /// <summary>
        ///     Call to About page and load the content
        /// </summary>
        /// <returns>About Page</returns>
        public ActionResult About() {
            ViewBag.Message = "TagManuel";

            return View();
        }

        /// <summary>
        ///     Contact Page Call
        /// </summary>
        /// <returns>Contact Page</returns>
        public ActionResult Contact() {
            ViewBag.Message = "Contact Page";

            return View();
        }

        /// <summary>
        ///     Get Page Call
        /// </summary>
        /// <returns>Get Page</returns>
        public ActionResult Get() {
            ViewBag.Message = "Get Repo Data";

            return View();
        }

        /// <summary>
        ///     Start page Call ( Load Repository Data of given reposid list)
        /// </summary>
        /// <returns>Start Page</returns>
        public async Task<ActionResult> Start() {
            //Load Repository ID's
            var fileString = System.IO.File.ReadAllText(@"E:\Github\tagged\idlist.txt");
            var fileArray = fileString.Split(',');
            //Get every single ID
            var fileArrayInt = new int[fileArray.Length];
            //Create List for api 'api.github.com/repos(itory)' call 
            var data3 = new List<Repo>();
            var a = 0;
            foreach (var file in fileArray) {
                fileArrayInt[a] = int.Parse(file);
                a++;
            }


            var accessToken = Session["OAuthToken"] as string;
            if (accessToken != null) {
                // This allows the client to make requests to the GitHub API on the user's behalf
                // without ever having the user's OAuth credentials.
                client.Credentials = new Credentials(accessToken);
            }
            //Create List's for every Api Call
            var tree = new List<TreeResponse>();
            var readmes = new List<Readme>();
            var language = new List<IReadOnlyList<RepositoryLanguage>>();
            var commits = new List<IReadOnlyList<GitHubCommit>>();
            var readeconn = new List<string>();
            var comments = new List<IReadOnlyList<CommitComment>>();
            var issues = new List<IReadOnlyList<Issue>>();
            var webClient = new WebClient();


            try {
                //not usefull call ,... but without the Api calls run without oAuth token
                var test2 = await client.Repository.GetAllForCurrent();
                // The following requests retrieves all of the user's repositories and
                // requires that the user be logged in to work.
                var options = new ApiOptions {PageCount = 10, PageSize = 100};
                //MAX : 100


                //Run through every ID in the File
                foreach (var id in fileArrayInt) {
                    //Debug.WriteLine(id);
                    //Debug.WriteLine(fileArrayInt.ToList().IndexOf(id));
                    try {
                        //Call Tree Api to get Git Structure (files and dirs) from master path
                        tree.Add(await client.Git.Tree.GetRecursive(id, "master"));
                    } catch (Exception e) {
                        tree.Add(new TreeResponse());
                    }
                    //Debug.WriteLine("Finish Tree");
                    //If Tree (master) empty -> empty Repository so do not make more request than it need fuel up other list with null data
                    if (tree[tree.Count - 1].Tree == null) {
                        //Debug.WriteLine("Empty Repository");
                        readmes.Add(new Readme());
                        readeconn.Add("");
                        language.Add(null);
                        commits.Add(null);
                        comments.Add(null);
                        issues.Add(null);
                        //But add other data about the repo
                        var shortTemp = await client.Repository.Get(id);
                        var tempPro = new Repo {
                            name = shortTemp.Name,
                            id = shortTemp.Id,
                            html_url = shortTemp.HtmlUrl,
                            full_name = shortTemp.FullName,
                            owner = {id = shortTemp.Owner.Id},
                            description = shortTemp.Description
                        };
                        //Debug.WriteLine("Add Data");
                        data3.Add(tempPro);
                        //go to next item 
                        continue;
                    }
                    try {
                        //Readme Call -> get Readme Name of Repo
                        readmes.Add(await client.Repository.Content.GetReadme(id));
                    } catch (Exception e) {
                        readmes.Add(new Readme());
                    }
                    if (readmes.Last() != null) {
                        try {
                           
                            var shortTemp = await client.Repository.Get(id);
                            //Add other data about the repo
                            var tempPro = new Repo {
                                name = shortTemp.Name,
                                id = shortTemp.Id,
                                html_url = shortTemp.HtmlUrl,
                                full_name = shortTemp.FullName,
                                owner = {id = shortTemp.Owner.Id},
                                description = shortTemp.Description
                            };

                            //Use normal WebClient to get Readme without APi Request ;)
                            //Debug.WriteLine("Add Data");
                            data3.Add(tempPro);
                            readeconn.Add(
                                          webClient.DownloadString(
                                                                   "https://raw.githubusercontent.com/"
                                                                   + tempPro.full_name + "/master/"
                                                                   + readmes.Last().Name));
                        } catch (Exception e) {
                            readeconn.Add("");
                        }
                    }

                    //Debug.WriteLine("Finish Readme");
                    try {
                        //Get Language of repo -> Language Api Call
                        language.Add(await client.Repository.GetAllLanguages(id));
                    } catch (Exception e) {
                        language.Add(null);
                    }
                    //Debug.WriteLine("Finish Language");
                    try {
                        //Get All commits ( with options) -> api call commits
                        commits.Add(await client.Repository.Commit.GetAll(id, options));
                    } catch (Exception e) {
                        commits.Add(null);
                    }
                    //Debug.WriteLine("Finish Commits");
                    try {
                        //Get All Comments with option -> Api call Comments
                        comments.Add(await client.Repository.Comment.GetAllForRepository(id, options));
                    } catch (Exception e) {
                        comments.Add(null);
                    }
                    //Debug.WriteLine("Finish Comments");
                    try {
                        //Get All Issues with option _> api call issues
                        issues.Add(await client.Issue.GetAllForRepository(id, options));
                    } catch (Exception e) {
                        issues.Add(null);
                    }
                    //Debug.WriteLine("Finish Issues");
                    Debug.WriteLine(
                                    "Reamaining Requests: " + client.GetLastApiInfo().RateLimit.Remaining + " "
                                    + (client.GetLastApiInfo().RateLimit.Reset.Hour + 1) + ":"
                                    + client.GetLastApiInfo().RateLimit.Reset.Minute);
                }
            } catch (AuthorizationException) {
                // Either the accessToken is null or it's invalid. This redirects
                // to the GitHub OAuth login page. That page will redirect back to the
                // Authorize action.
                return Redirect(GetOauthLoginUrl());
            }
            //Create List's without 'null' entry looks a bit ugly becouse of overlength and yeah it can be look nicer but so gives no problem
            var re = new Repo();
            var complete = new JSONFullData[fileArrayInt.Length];
            for (var i = 0; i < fileArrayInt.Length; i++) {
                Debug.WriteLine("Create JSONFull: " + i);
                var temp_language = new List<Language>();
                var temp_repro = new List<Repro>();
                var temp_commits = new List<Commits>();
                var temp_comments = new List<Comments>();
                var temp_issues = new List<Models.Issue>();
                if (language[i] != null) {
                    temp_language.AddRange(
                                           language[i].Select(
                                                              te =>
                                                                  new Language(
                                                                               te.Name ?? "",
                                                                               te.NumberOfBytes != 0
                                                                                   ? te.NumberOfBytes : 0)));
                } else {
                    temp_language.Add(new Language("", 0));
                }
                if (tree[i].Tree != null) {
                    temp_repro.AddRange(tree[i].Tree.Select(te => new Repro(te.Path ?? "", te.Type.ToString())));
                } else {
                    temp_repro.Add(new Repro("", ""));
                }
                if (commits[i] != null) {
                    temp_commits.AddRange(
                                          commits[i].Select(
                                                            te =>
                                                                new Commits(
                                                                            new Commit(
                                                                                       new Author(
                                                                                                  te.Commit.Author
                                                                                                  != null
                                                                                                      ? te.Commit.Author
                                                                                                          .Name : "",
                                                                                                  te.Commit.Author
                                                                                                  != null
                                                                                                      ? te.Commit.Author
                                                                                                          .Email : ""),
                                                                                       new Author(
                                                                                                  te.Commit.Committer
                                                                                                  != null
                                                                                                      ? te.Commit
                                                                                                          .Committer
                                                                                                          .Name : "",
                                                                                                  te.Commit.Committer
                                                                                                  != null
                                                                                                      ? te.Commit
                                                                                                          .Committer
                                                                                                          .Email : ""),
                                                                                       te.Commit.Message ?? ""),
                                                                            te.Author != null ? te.Author.Login : "",
                                                                            te.Committer != null
                                                                                ? te.Committer.Login : "")));
                } else {
                    temp_commits.Add(new Commits(new Commit(new Author("", ""), new Author("", ""), ""), "", ""));
                }
                if (comments[i] != null) {
                    temp_comments.AddRange(
                                           comments[i].Select(
                                                              te =>
                                                                  new Comments(
                                                                               te.Body ?? "",
                                                                               te.Path ?? "",
                                                                               new Author(
                                                                                          te.User != null
                                                                                              ? te.User.Login : "",
                                                                                          ""))));
                } else {
                    temp_comments.Add(new Comments("", "", new Author("", "")));
                }
                if (issues[i] != null) {
                    temp_issues.AddRange(
                                         issues[i].Select(
                                                          te =>
                                                              new Models.Issue(
                                                                               te.State == ItemState.Open
                                                                                   ? "open" : "closed",
                                                                               te.Title ?? "",
                                                                               te.Body ?? "",
                                                                               new Author(te.User.Name ?? "", ""))));
                } else {
                    temp_issues.Add(new Models.Issue("", "", "", new Author("", "")));
                }
                //add all list in one big list ... see too mutch list,but there is no need for
                complete[i] = new JSONFullData(
                                               data3[i].id,
                                               data3[i].name,
                                               data3[i].full_name,
                                               data3[i].owner.id,
                                               data3[i].description,
                                               readeconn[i] != null ? readeconn[i] : "",
                                               temp_language.ToArray(),
                                               temp_repro.ToArray(),
                                               tree[i].Truncated,
                                               temp_commits.ToArray(),
                                               temp_comments.ToArray(),
                                               temp_issues.ToArray());
            }
            //Create Json String
            var json = JsonConvert.SerializeObject(complete);
            //json = json.Replace("},{", "},\n{");
            //Write Json file
            System.IO.File.WriteAllText(@"E:\Github\tagged\jsontest.json", json);

            //Get Remaining Api calls, try it 
            try {
                re.name = "Remaining: " + client.GetLastApiInfo().RateLimit.Remaining + " Reset Time: "
                    + (client.GetLastApiInfo().RateLimit.Reset.Hour + 1) + ":"
                    + client.GetLastApiInfo().RateLimit.Reset.Minute + ":"
                    + client.GetLastApiInfo().RateLimit.Reset.Second;
            } catch (NullReferenceException e) {
                re.name =
                    "Last Element was may a empty Repository (but look). So there is no Api Info ... sadly this catch it hoply.  "
                    + e.Message;
            }

            //Add this to the list's so it will show up on the page
            data3.Add(re);
            tree.Add(new TreeResponse());
            readmes.Add(new Readme());
            language.Add(null);
            commits.Add(null);
            readeconn.Add("");
            comments.Add(null);
            issues.Add(null);
            var teview = new ViewRepoOverview(
                                              data3.ToArray(),
                                              tree.ToArray(),
                                              readmes.ToArray(),
                                              language.ToArray(),
                                              commits.ToArray(),
                                              readeconn.ToArray(),
                                              comments.ToArray(),
                                              issues.ToArray());

            return View(teview);
        }
    }
}