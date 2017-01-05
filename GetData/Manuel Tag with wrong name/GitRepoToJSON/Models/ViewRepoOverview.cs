using Octokit;
using System.Collections.Generic;

namespace GitRepoToJSON.Models {
    /// <summary>
    /// View Class to Create ViewObject for the cshtml file
    /// </summary>
    public class ViewRepoOverview {
        /// <summary>
        /// Constructor with Repositories Object
        /// </summary>
        /// <param name="repositories">An array with Repositories Objects</param>
        public ViewRepoOverview(Repo[] repositories)
        {
            Repositories = repositories;
        }

        /// <summary>
        /// Constructor with Repos and TreeResponse Objects
        /// </summary>
        /// <param name="repos">An array with Repositories Objects</param>
        /// <param name="treeResponses">Array full with TreeResponse Objects</param>
        public ViewRepoOverview(Repo[] repos, TreeResponse[] treeResponses)
        {
            Repositories = repos;
            Tree = treeResponses;
        }

        /// <summary>
        /// Constructor with Repositories, TreeResponse, Readme, Language and Commits Objects
        /// </summary>
        /// <param name="repos">An array with Repositories Objects</param>
        /// <param name="treeResponses">Array full with TreeResponse Objects</param>
        /// <param name="readmes">Readme Files with it name and Content</param>
        /// <param name="language">Language Object Array</param>
        /// <param name="gitHubCommits">Commit Object Array</param>
        public ViewRepoOverview(Repo[] repos, TreeResponse[] treeResponses, Readme[] readmes, IReadOnlyList<RepositoryLanguage>[] language, IReadOnlyList<GitHubCommit>[] gitHubCommits)
        {
            Repositories = repos;
            Tree = treeResponses;
            Readmes = readmes;
            Languagen = language;
            CommitS = gitHubCommits;
        }

        /// <summary>
        /// Constructor for full view use
        /// </summary>
        /// <param name="repos">An array with Repositories Objects</param>
        /// <param name="treeResponses">Array full with TreeResponse Objects</param>
        /// <param name="readmes">Readme Files with it name and Content</param>
        /// <param name="language">Language Object Array</param>
        /// <param name="gitHubCommits">Commit Object Array</param>
        /// <param name="readmeCon">readmeCon</param>
        /// <param name="commitComments">Commit Comments Array</param>
        /// <param name="issues">Issue Array</param>
        public ViewRepoOverview(Repo[] repos, TreeResponse[] treeResponses, Readme[] readmes, IReadOnlyList<RepositoryLanguage>[] language, IReadOnlyList<GitHubCommit>[] gitHubCommits, string[] readmeCon, IReadOnlyList<CommitComment>[] commitComments, IReadOnlyList<Octokit.Issue>[] issues)
        {
            Repositories = repos;
            Tree = treeResponses;
            Readmes = readmes;
            Languagen = language;
            CommitS = gitHubCommits;
            ReadmeCon = readmeCon;
            Comments = commitComments;
            Issues = issues;
        }
        /// <summary>
        /// Repositories Object
        /// </summary>
        public Repo[] Repositories { get; private set; }
        /// <summary>
        /// TreeResponse Object
        /// </summary>
        public TreeResponse[] Tree { get; private set; }
        /// <summary>
        /// Readme Object
        /// </summary>
        public Readme[] Readmes { get; private set; }
        /// <summary>
        /// language Object
        /// </summary>
        public IReadOnlyList<RepositoryLanguage>[] Languagen { get; private set; }
        /// <summary>
        /// Commit Object
        /// </summary>
        public IReadOnlyList<GitHubCommit>[] CommitS { get; private set; }
        /// <summary>
        /// ReadmeCon Object
        /// </summary>
        public string[] ReadmeCon { get; private set; }
        /// <summary>
        /// CommitComments Object
        /// </summary>
        public IReadOnlyList<CommitComment>[] Comments { get; private set; }
        //Issue Object from Octokit
        public IReadOnlyList<Octokit.Issue>[] Issues { get; private set; }

    }

}