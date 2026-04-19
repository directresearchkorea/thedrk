# GitHub Deployment & CMS Setup To-Do

The project has been migrated to static HTML and a web-based CMS (`Sveltia CMS`) has been added to the `/write` directory. 
The user will upload the local folder to GitHub soon. Once the user provides the GitHub Repository URL, the following tasks must be executed:

- [ ] **Configure Web CMS**: Update `write/config.yml` with the user's actual GitHub `username/repository` (e.g., `ggamy/thedrk.com`).
- [ ] **Verify GitHub Actions**: Ensure `.github/workflows/build-blog.yml` is committed and triggers correctly on the repository.
- [ ] **Custom Domain Configuration**: Guide the user through setting up Gabia DNS records to point `www.thedrk.com` to the GitHub Pages IP addresses.
- [ ] **Verify Web CMS Login**: Confirm the user can access `www.thedrk.com/write` and authenticate via GitHub.
