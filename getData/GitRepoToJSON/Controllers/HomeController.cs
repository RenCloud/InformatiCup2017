using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net;
using System.Threading.Tasks;
using System.Web.Caching;
using System.Web.Mvc;
using System.Web.Security;
using GitRepoToJSON.Models;
using Newtonsoft.Json;
using Octokit;
using Author = GitRepoToJSON.Models.Author;
using Issue = Octokit.Issue;
using Language = GitRepoToJSON.Models.Language;


namespace GitRepoToJSON.Controllers
{
    public class HomeController : Controller {
        private const string ClientId = "";

        private const string ClientSecret = "";

        private readonly GitHubClient client = new GitHubClient(new ProductHeaderValue(""));

        public ActionResult Index() {
            return View();
        }
        // This is the Callback URL that the GitHub OAuth Login page will redirect back to.
        public async Task<ActionResult> Authorize(string code, string state)
        {
            if (string.IsNullOrEmpty(code)) {
                return RedirectToAction("Index");
            }
            var expectedState = Session["CSRF:State"] as string;
            if (state != expectedState)
            {
                throw new InvalidOperationException("SECURITY FAIL!");
            }
            Session["CSRF:State"] = null;

            var token = await client.Oauth.CreateAccessToken(new OauthTokenRequest(ClientId, ClientSecret, code));
            Session["OAuthToken"] = token.AccessToken;

            return RedirectToAction("Index");
        }

        private string GetOauthLoginUrl()
        {
            var csrf = Membership.GeneratePassword(24, 1);
            Session["CSRF:State"] = csrf;

            // 1. Redirect users to request GitHub access
            var request = new OauthLoginRequest(ClientId)
            {
                Scopes = { "user", "notifications", "repo", "repo:status", "public_repo" },
                State = csrf
            };
            var oauthLoginUrl = client.Oauth.GetGitHubLoginUrl(request);
            return oauthLoginUrl.ToString();
        }

        public ActionResult About() {
            ViewBag.Message = "Your application description page.";

            return View();
        }

        public ActionResult Contact() {
            ViewBag.Message = "Your contact page.";

            return View();
        }

        public ActionResult Get() {
            ViewBag.Message = "Get More Repos";

            return View();
        }

        public async Task<ActionResult> Start() {
            ViewBag.Message = "100 ID Downloaded";
            var directory = new DirectoryInfo(@"E:\Github\fortschrit");
            var idPreFile = 0;
            var currentID = 0;
            var directoryFiles = directory.GetFiles();
            if (directoryFiles.Length != 0)
            {
                currentID = int.Parse(directoryFiles[0].Name);
                idPreFile = currentID;
            }
            directory = new DirectoryInfo(@"E:\Github\id");
            directoryFiles = directory.GetFiles();
            var data = new List<Repo[]>();
            var data3 = new List<Repo>();
            var found = false;
            foreach (var file in directoryFiles)
            {
                if (int.Parse(file.Name) != currentID)
                {
                    continue;
                }
                data.Add(JsonConvert.DeserializeObject<Repo[]>(System.IO.File.ReadAllText(file.FullName)));
                var data2 = data.SelectMany(arry => arry).ToList();
                data3.AddRange(from repos in data2 where repos.id >= currentID select (repos));
                found = true;
                break;
            }
            if (!found)
            {
                var request = (HttpWebRequest)WebRequest.Create("https://api.github.com/repositories?since=" + currentID);
                //request.UserAgent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10";
                request.UserAgent = "Mozilla";
                request.KeepAlive = false;
                request.Method = "GET";
                var response = (HttpWebResponse)request.GetResponse();
                var newFile = new StreamReader(response.GetResponseStream()).ReadToEnd();
                var datadada = JsonConvert.DeserializeObject<Repo[]>(newFile);
                System.IO.File.WriteAllText(@"E:\Github\id\" + datadada[0].id, newFile);
                directory = new DirectoryInfo(@"E:\Github\id");
                directoryFiles = directory.GetFiles();
                currentID = datadada[0].id;
                foreach (var file in directoryFiles)
                {
                    if (int.Parse(file.Name) != currentID)
                    {
                        continue;
                    }
                    data.Add(JsonConvert.DeserializeObject<Repo[]>(System.IO.File.ReadAllText(file.FullName)));
                    var data2 = data.SelectMany(arry => arry).ToList();
                    data3.AddRange(from repos in data2 where repos.id >= currentID select (repos));
                    break;
                }

            }

            var accessToken = Session["OAuthToken"] as string;
            if (accessToken != null)
            {
                // This allows the client to make requests to the GitHub API on the user's behalf
                // without ever having the user's OAuth credentials.
                client.Credentials = new Credentials(accessToken);
            }

            var tree = new List<TreeResponse>();
            var readmes = new List<Readme>();
            var language = new List<IReadOnlyList<RepositoryLanguage>>();
            var commits = new List<IReadOnlyList<GitHubCommit>>();
            var readeconn = new List<string>();
            var comments = new List<IReadOnlyList<CommitComment>>();
            var issues = new List<IReadOnlyList<Issue>>();
            var webClient = new WebClient();


            try
            {
                var test2 = await client.Repository.GetAllForCurrent();
                // The following requests retrieves all of the user's repositories and
                // requires that the user be logged in to work.
                var options = new ApiOptions { PageCount = 10, PageSize = 100 };
                //MAX : 100



                foreach (var id in data3)
                {
                    Debug.WriteLine(id.id);
                    try
                    {
                        tree.Add(await client.Git.Tree.GetRecursive(id.id, "master"));
                    }
                    catch (Exception e)
                    {
                        tree.Add(new TreeResponse());
                    }
                    Debug.WriteLine("Finish Tree");
                    if (tree[tree.Count - 1].Tree == null)
                    {
                        Debug.WriteLine("Empty Repository");
                        readmes.Add(new Readme());
                        readeconn.Add("");
                        language.Add(null);
                        commits.Add(null);
                        comments.Add(null);
                        issues.Add(null);


                        continue;

                    }
                    try
                    {
                        readmes.Add(await client.Repository.Content.GetReadme(id.id));
                    }
                    catch (Exception e)
                    {
                        readmes.Add(new Readme());
                    }
                    if (readmes.Last() != null)
                    {
                        try
                        {
                            readeconn.Add(
                                          webClient.DownloadString(
                                                            "https://raw.githubusercontent.com/" + id.full_name
                                                            + "/master/" + readmes.Last().Name));
                        }
                        catch (Exception e)
                        {
                            readeconn.Add("");
                        }
                    }
                    Debug.WriteLine("Finish Readme");
                    try
                    {
                        language.Add(await client.Repository.GetAllLanguages(id.id));
                    }
                    catch (Exception e)
                    {
                        language.Add(null);
                    }
                    Debug.WriteLine("Finish Language");
                    try
                    {
                        commits.Add(await client.Repository.Commit.GetAll(id.id, options));
                    }
                    catch (Exception e)
                    {
                        commits.Add(null);
                    }
                    Debug.WriteLine("Finish Commits");
                    try
                    {
                        comments.Add(await client.Repository.Comment.GetAllForRepository(id.id, options));
                    }
                    catch (Exception e)
                    {
                        comments.Add(null);
                    }
                    Debug.WriteLine("Finish Comments");
                    try
                    {
                        issues.Add(await client.Issue.GetAllForRepository(id.id, options));
                    }
                    catch (Exception e)
                    {
                        issues.Add(null);
                    }
                    Debug.WriteLine("Finish Issues");
                    Debug.WriteLine("Reamaining Requests: " + client.GetLastApiInfo().RateLimit.Remaining + " " + (client.GetLastApiInfo().RateLimit.Reset.Hour + 1) + ":" + (client.GetLastApiInfo().RateLimit.Reset.Minute));
                }

            }
            catch (AuthorizationException)
            {
                // Either the accessToken is null or it's invalid. This redirects
                // to the GitHub OAuth login page. That page will redirect back to the
                // Authorize action.
                return Redirect(GetOauthLoginUrl());
            }
            var re = new Repo();
            var complete = new JSONFullData[data3.Count];
            for (var i = 0; i < data3.Count; i++)
            {
                Debug.WriteLine("Create JSONFull: " + i);
                var temp_language = new List<Language>();
                var temp_repro = new List<Repro>();
                var temp_commits = new List<Commits>();
                var temp_comments = new List<Comments>();
                var temp_issues = new List<Models.Issue>();
                if (language[i] != null)
                {
                    temp_language.AddRange(language[i].Select(te => new Language(te.Name ?? "", te.NumberOfBytes != 0 ? te.NumberOfBytes : 0)));
                }
                else
                {
                    temp_language.Add(new Language("", 0));
                }
                if (tree[i].Tree != null)
                {
                    temp_repro.AddRange(tree[i].Tree.Select(te => new Repro(te.Path ?? "", te.Type.ToString())));
                }
                else
                {
                    temp_repro.Add(new Repro("", ""));
                }
                if (commits[i] != null)
                {
                    temp_commits.AddRange(commits[i].Select(te => new Commits(new Models.Commit(new Author(te.Commit.Author != null ? te.Commit.Author.Name : "", te.Commit.Author != null ? te.Commit.Author.Email : ""), new Author(te.Commit.Committer != null ? te.Commit.Committer.Name : "", te.Commit.Committer != null ? te.Commit.Committer.Email : ""), te.Commit.Message ?? ""), te.Author != null ? te.Author.Login : "", te.Committer != null ? te.Committer.Login : "")));
                }
                else
                {
                    temp_commits.Add(new Commits(new Models.Commit(new Author("", ""), new Author("", ""), ""), "", ""));
                }
                if (comments[i] != null)
                {
                    temp_comments.AddRange(comments[i].Select(te => new Comments(te.Body ?? "", te.Path ?? "", new Author(te.User != null ? te.User.Login : "", ""))));
                }
                else
                {
                    temp_comments.Add(new Comments("", "", new Author("", "")));
                }
                if (issues[i] != null)
                {
                    temp_issues.AddRange(issues[i].Select(te => new Models.Issue(te.State == ItemState.Open ? "open" : "closed", te.Title ?? "", te.Body ?? "", new Author(te.User.Name ?? "", ""))));
                }
                else
                {
                    temp_issues.Add(new Models.Issue("", "", "", new Author("", "")));
                }
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

            var json = JsonConvert.SerializeObject(complete);
            //json = json.Replace("},{", "},\n{");
            System.IO.File.WriteAllText(@"E:\Github\ausgabe\" + currentID + "-" + data3[data3.Count - 1].id + ".json", json);
            System.IO.File.Delete(@"E:\Github\fortschrit\" + idPreFile);
            System.IO.File.WriteAllText(@"E:\Github\fortschrit\" + data3[data3.Count - 1].id, "");
            try
            {
                re.name = "Remaining: " + client.GetLastApiInfo().RateLimit.Remaining + " Reset Time: "
                    + (client.GetLastApiInfo().RateLimit.Reset.Hour + 1) + ":"
                    + client.GetLastApiInfo().RateLimit.Reset.Minute + ":"
                    + client.GetLastApiInfo().RateLimit.Reset.Second;

            }
            catch (NullReferenceException e)
            {
                re.name =
                    "Last Element was may a empty Repository (but look). So there is no Api Info ... "
                    + e.Message;
            }


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
